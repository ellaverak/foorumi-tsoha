from app import app
from flask import render_template, request, redirect
import users, topics, thread

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
    return render_template("topic.html", topic=top, topic_id=id)
    
@app.route("/thread<int:id>")
def show_thread(id):
    thre = list(thread.show_thread(id))
    return render_template("thread.html", thread=thre, thread_id=id)
    
@app.route("/new<int:id>")
def new_thread(id):
    return render_template("new_thread.html", topic_id=id)

@app.route("/create_new", methods=["POST"])
def create_new_thread():
    title = request.form["title"]
    op_content = request.form["op_content"]
    topic_id = request.form["topic_id"]
    if thread.create_thread(title, op_content, topic_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Langan luominen ei onnistunut")
    
@app.route("/reply", methods=["POST"])
def reply():
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    if thread.reply(content, thread_id):
        return redirect("/thread"+str(thread_id))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")
    
