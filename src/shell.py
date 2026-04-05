import sys
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import RichLog, Header, Footer
from textual.containers import Vertical
from textual_terminal import Terminal
from rich.text import Text
import threading

class DiscordTUI(App):
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

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield RichLog(id="bot_logs", highlight=True, markup=True)
            yield Terminal(command="bash", id="shell")
        yield Footer()

    async def on_mount(self) -> None:
        log_widget = self.query_one("#bot_logs", RichLog)
        
        terminal_widget = self.query_one("#shell", Terminal)
        terminal_widget.start()

        class LogRedirector:
            def write(self, data):
                if data.strip():
                    log_widget.write(
                        Text.from_ansi(data.strip())
                    )
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
    app = DiscordTUI(bot, token)
    await app.run_async()
