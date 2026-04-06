import sys
import asyncio
import code
import contextlib
import io
import threading

from textual.app import App, ComposeResult
from textual.widgets import RichLog, Header, Footer, Input
from textual.containers import Vertical
from textual import on
from rich.text import Text

class PythonREPL(Input):
    def __init__(self, id, output_widget, locals_dict):
        self.output = output_widget
        self.console = code.InteractiveConsole(locals=locals_dict)

        super().__init__(id=id, placeholder=">>> ")
    def set_log(self, v):
        self.output=v
    @on(Input.Submitted)
    async def handle_submit(self, event: Input.Submitted) -> None:
        code_input = event.value
        self.value = ""

        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            try:
                more = self.console.push(code_input)
            except Exception as e:
                self.output.write(f"[bold red]{e}[/]")
                return

        output = buffer.getvalue()
        if output:
            self.output.write(Text.from_ansi(output.rstrip()))

        self.placeholder = "... " if more else ">>> "

class UmamusumeTUI(App):
    CSS = """
    RichLog {
        height: 1fr;
        border: solid green;
    }
    Terminal {
        height: 1fr;
        border: solid blue;
    }
    """

    def __init__(self, bot, token):
        super().__init__()
        self.bot = bot
        self.token = token

    def on_unmount(self) -> None:
        self.bot.save()

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="bot_logs", highlight=True, markup=True)
            yield RichLog(id="repl_output", highlight=True, markup=True, auto_scroll=True)
            yield PythonREPL(id="repl", output_widget=None, locals_dict={})
        yield Footer()
        
    async def on_mount(self) -> None:
        log_widget = self.query_one("#bot_logs", RichLog)
        repl_output = self.query_one("#repl_output", RichLog)
        repl = self.query_one("#repl", PythonREPL)
        
        repl.output = repl_output
        
        repl.console.locals.update({
            "app": self,
            "uma": self.bot,
            "log": log_widget
        })
        class LogRedirector:
            def write(self, data):
                if data.strip():
                    log_widget.write(
                        Text.from_ansi(data.strip())
                    )
                    log_widget.scroll_end()
            def flush(self): pass

        sys.stdout = LogRedirector()

        print("Starting bot")

        try:
            threading.Thread(
                target=self.bot.run,
                args=(self.token,),
                daemon=True
            ).start()
        except Exception as e:
            log_widget.write(f"[bold red]Bot Error: {e}[/]")
        
async def start_bot(bot, token):
    app = UmamusumeTUI(bot, token)
    await app.run_async()
