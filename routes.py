from app import app
from flask import render_template, request, redirect
import users

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
        
    if request.method == "POST":
    	username = request.form["username"]
    	password1 = request.form["password1"]
    	password2 = request.form["password2"]
    	if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
    	if users.register(username, password1):
            return redirect("/")
    	else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
