import os
from quart import Quart, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

DEV_PASSWORD = os.getenv("DASHBOARD_PASSWORD")
app=Quart(__name__)
app.secret_key="6767"

@app.route("/", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form
        submitted_password = form.get("password")
        
        if submitted_password == DEV_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        
        return await render_template("login.html", error="Invalid backend password!")
    
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
        
    return await render_template("login.html")

@app.route("/dashboard")
async def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    return await render_template("dashboard.html")

if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
