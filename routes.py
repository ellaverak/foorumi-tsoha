from os import abort
import thread
from flask import render_template, request, redirect, session
import users
import topics
import reply
from app import app


@app.context_processor
def inject_users():
    all_users = users.get_users()
    return dict(all_users=all_users)


@app.context_processor
def inject_topics():
    topic_list = topics.get_list()
    return dict(topic_list=topic_list)


@app.route("/")
def index():
    topics_ = topics.get_topics()
    return render_template("index.html", topics=topics_)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if len(username) == 0:
            return render_template("error.html", message="Kirjoita käyttäjänimi")
        if len(password1) < 4 or len(password2) < 4:
            return render_template("error.html",
                                   message="Salasanan on oltava vähintään neljän merkin pituinen")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjänimi on jo käytössä")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect(request.referrer)
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect(request.referrer)


@app.route("/topics<int:id>")
def show_topic(id):
    topic = topics.show_topic(id)
    secret = topics.get_secret(id)
    users_ = users.get_secret_users(id)
    if secret == 0:
        return render_template("topic.html", topic=topic, topic_id=id, users=users_)
    else:
        if users.access(id):
            return render_template("topic.html", topic=topic, topic_id=id, users=users_)
        else:
            return render_template("error.html", message="Sinulla ei ole pääsyä alueelle")


@app.route("/thread<int:id>")
def show_thread(id):
    thread_ = thread.show_thread(id)[0]
    replies_ = thread.show_thread(id)[1]
    topic_info = topics.get_info_thread(id)
    print(topic_info)
    if topic_info[0][1] == 0:
        return render_template("thread.html", thread=thread_, replies=replies_,
                               thread_id=id, topic_info=topic_info)
    else:
        if users.access(topic_info[0][2]):
            return render_template("thread.html", thread=thread_, replies=replies_,
                                   thread_id=id, topic_info=topic_info)
        else:
            return render_template("error.html", message="Sinulla ei ole pääsyä ketjuun")


@app.route("/new<int:id>")
def new_thread(id):
    topic_info = topics.get_info_topic(id)
    return render_template("new_thread.html", topic_id=id, topic_info=topic_info)


@app.route("/create_new", methods=["POST"])
def create_new_thread():
    if session.get("user_id", 0) == 0:
        return render_template("error.html",
                               message="Vain kirjautunut käyttäjä voi luoda uuden ketjun")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    title = request.form["title"]
    op_content = request.form["op_content"]
    topic_id = request.form["topic_id"]
    if len(title) == 0:
        return render_template("error.html", message="Kirjoita ketjulle otsikko")
    if len(op_content) == 0:
        return render_template("error.html", message="Kirjoita aloitusviesti")
    result = thread.create_thread(title, op_content, topic_id)
    if result[0]:
        return redirect("/thread"+str(result[1]))
    else:
        return render_template("error.html", message="Ketjun luominen ei onnistunut")


@app.route("/reply", methods=["POST"])
def reply_to():
    if session.get("user_id", 0) == 0:
        return render_template("error.html",
                               message="Vain kirjautunut käyttäjä voi lähettää viestin")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    thread_id = request.form["thread_id"]
    if len(content) == 0:
        return render_template("error.html", message="Kirjoita viesti")
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    reply_id = request.form["reply_id"]
    thread_id = request.form["thread_id"]
    if len(content) == 0:
        return render_template("error.html", message="Kirjoita viesti")
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    title = request.form["title"]
    op_content = request.form["op_content"]
    thread_id = request.form["thread_id"]
    if len(title) == 0:
        return render_template("error.html", message="Kirjoita ketjulle otsikko")
    if len(op_content) == 0:
        return render_template("error.html", message="Kirjoita aloitusviesti")
    if thread.edit_thread(title, op_content, thread_id):
        return redirect("/thread"+str(thread_id))
    else:
        return render_template("error.html", message="Ketjun muokkaus ei onnistunut")


@app.route("/topic_options")
def topic_options():
    users_ = users.get_users()
    topics_ = topics.get_list()
    return render_template("topic_options.html", users=users_, topics=topics_)


@app.route("/delete_topic", methods=["POST"])
def delete_topic():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    topic_name = request.form["topic_name"]
    if len(topic_name) == 0:
        return render_template("error.html", message="Kirjoita alueen nimi")
    if topics.delete_topic(topic_name):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Alueen poisto ei onnistunut. \
        Syy: Virhe tai perusalueen poistokäsky.")


@app.route("/create_topic", methods=["POST"])
def create_topic():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    topic_name = request.form["topic_name"]
    if len(topic_name) == 0:
        return render_template("error.html", message="Kirjoita alueen nimi")
    result = topics.create_topic(topic_name)
    if result[0]:
        return redirect("/topics"+str(result[1]))
    else:
        return render_template("error.html", message="Alueen luonti ei onnistunut")


@app.route("/secret_topics")
def secret_topics():
    s_topic = topics.get_secret_topics()
    users_ = users.get_users()
    return render_template("secret_topics.html", s_topics=s_topic, users=users_)


@app.route("/create_secret_topic", methods=["POST"])
def create_secret():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    topic_name = request.form["topic_name"]
    choises = request.form["choises"]
    if len(topic_name) == 0:
        return render_template("error.html", message="Kirjoita alueen nimi")
    result = topics.create_secret_topic(topic_name, choises)
    if result[0]:
        return redirect("/topics"+str(result[1]))
    else:
        return render_template("error.html", message="Salaisen alueen luonti ei onnistunut")


@app.route("/result", methods=["POST", "GET"])
def result():
    if session.get("user_id", 0) == 0:
        return render_template("error.html",
                               message="Vain kirjautunut käyttäjä voi käyttää hakutoimintoa")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    query = request.form["query"]
    if query == "":
        return render_template("error.html",
                               message="Tyhjä hakukenttä")
    replies = reply.search(query)
    return render_template("result.html", replies=replies)


@app.route("/add_secret_users", methods=["POST"])
def add_secret():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    choises = request.form["choises"]
    topic_id = request.form["topic_id"]
    if users.add_secret(topic_id, choises):
        return redirect("/topics"+str(topic_id))
    else:
        return render_template("error.html", message="Käyttäjien lisääminen ei onnistunut")
