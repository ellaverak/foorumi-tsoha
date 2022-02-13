from app import app
from flask import render_template, request, redirect, url_for
import users, topics, thread, reply

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
    user = list(users.get_secret_users(id))
    return render_template("topic.html", topic=top, topic_id=id, users=user)
    
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
    result = thread.create_thread(title, op_content, topic_id)
    if result[0]:
        return redirect("/thread"+str(result[1]))
    else:
        return render_template("error.html", message="Langan luominen ei onnistunut")
    
@app.route("/reply", methods=["POST"])
def reply_to():
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    if reply.leave_reply(content, thread_id):
        return redirect("/thread"+str(thread_id))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")
        
@app.route("/delete_reply<int:id>")
def delete_reply(id):
    result = reply.delete_reply(id)
    if result[0]:
        return redirect("/thread"+str(result[1]))
    else:
        return render_template("error.html", message="Viestin poistaminen ei onnistunut")
        
    
@app.route("/edit_reply", methods=["POST"])
def edit_reply():
    content = request.form["content"]
    reply_id = request.form["reply_id"]
    thread_id = request.form["thread_id"]
    if reply.edit_reply(content, reply_id):
        return redirect("/thread"+str(thread_id))
    else:
        return render_template("error.html", message="Viestin muokkaus ei onnistunut")
        
@app.route("/delete_thread<int:id>")
def delete_thread(id):
    result = thread.delete_thread(id)
    if result[0]:
        return redirect("/topics"+str(result[1]))
    else:
        return render_template("error.html", message="Ketjun poistaminen ei onnistunut")

@app.route("/edit_thread", methods=["POST"])
def edit_thread():
    title = request.form["title"]
    op_content = request.form["op_content"]
    thread_id = request.form["thread_id"]
    if thread.edit_thread(title, op_content, thread_id):
        return redirect("/thread"+str(thread_id))
    else:
        return render_template("error.html", message="Ketjun muokkaus ei onnistunut")
    
@app.route("/topic_options")
def topic_options():
    user = users.get_users()
    return render_template("topic_options.html", users=user)
    
@app.route("/delete_topic", methods=["POST"])   
def delete_topic():
    topic_name = request.form["topic_name"]
    if topics.delete_topic(topic_name):
        return redirect("/")
    else:
        return render_template("error.html", message="Alueen poisto ei onnistunut. Syy: Virhe tai perusalueen poistokäsky.")
    
@app.route("/create_topic", methods=["POST"])
def create_topic():
    topic_name = request.form["topic_name"]
    result = topics.create_topic(topic_name)
    if result[0]:
        return redirect("/topics"+str(result[1]))
    else:
        return render_template("error.html", message="Alueen luonti ei onnistunut")        

@app.route("/secret_topics")
def secret_topics():
    s_topic = list(topics.get_secret_topics())
    user = users.get_users()
    return render_template("secret_topics.html", s_topics=s_topic, users=user)
    
@app.route("/access<int:id>")
def access(id):
    if users.access(id):
        return redirect("/topics"+str(id))
    else:
        return render_template("error.html", message="Sinulla ei ole pääsyä alueelle")

@app.route("/create_secret_topic", methods=["POST"])
def create_secret():
    topic_name = request.form["topic_name"]
    choises = request.form["choises"]
    result = topics.create_secret_topic(topic_name, choises)
    if result[0]:
        return redirect("/topics"+str(result[1]))
    else:
        return render_template("error.html", message="Salaisen alueen luonti ei onnistunut")  

@app.route("/result")
def result():
    query = request.args["query"]
    replies = reply.search(query)
    return render_template("result.html", replies=replies)

@app.route("/add_secret_users", methods=["POST"])
def add_secret():
    choises = request.form["choises"]
    topic_id = request.form["topic_id"]
    if users.add_secret(topic_id, choises):
        return redirect("/")
    else:
        return render_template("error.html", message="Salaisen alueen luonti ei onnistunut")

@app.route("/back")
def back():
    return redirect("/")
    
        
