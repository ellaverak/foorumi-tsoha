from app import app
from flask import render_template, request, redirect
import users
import topics
import thread

@app.route("/")
def index():
    topic = list(topics.get_topics())
    return render_template("index.html", topics=topic)
    
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/topics<int:id>")
def show_topic(id):
    top = list(topics.show_topic(id))
    return render_template("topic.html", topic=top)
    
@app.route("/thread<int:id>")
def show_thread(id):
    thre = list(thread.show_thread(id))
    return render_template("thread.html", thread=thre)
    
