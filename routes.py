"""Module responsible of routing"""

from app import app
from flask import render_template, redirect, request, url_for, abort
import users, threads

@app.route("/")
def index():
    category_list = threads.get_categories()
    return render_template("index.html", categories=category_list)

@app.route("/<string:category>")
def topics(category):
    category_id = threads.get_category_id(category)
    topic_list = threads.get_topics(category_id)
    return render_template("topic.html", topics=topic_list, category=category)

@app.route("/<string:category>/<string:topic>")
def messages(category, topic):
    topic_id = threads.get_topic_id(topic)
    messages = threads.get_messages(topic_id)
    return render_template("messages.html", messages=messages, topic=topic, category=category)

@app.route("/new_topic", methods=["GET", "POST"])
def new_topic():
    if request.method == "GET":
        category = request.args["category"]
        return render_template("new_topic.html", category=category)
    if request.method == "POST":
        new_topic = request.form["new_topic"]
        category = request.form["category"]
        content = request.form["content"]
        category_id = threads.get_category_id(category)
        if users.session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if threads.save_new_topic(category_id, new_topic, content, users.get_user_id()):
            return redirect(url_for("messages", category=category, topic=new_topic))
        else:
            return render_template("error.html", message="Uuden aiheen luonti ei onnistunut") 

@app.route("/add", methods=["POST"])
def add_message():
    topic = request.form["topic"]
    category = request.form["category"]
    content = request.form["content"]
    topic_id = threads.get_topic_id(topic)
    if users.session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if threads.save_new_message(content, topic_id, users.get_user_id()):
        return redirect(url_for("messages", category=category, topic=topic))
    else: 
        return render_template("error.html", message="Viestin lähettäminen ei onnistunut")

@app.route("/remove_message", methods=["POST"])
def remove_message():
    message_id = request.form["message_id"]
    user_id = request.form["user_id"]
    topic = request.form["topic"]
    category = request.form["category"]
    if users.session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if threads.remove_message(message_id, user_id):
        return redirect(url_for("messages", category=category, topic=topic))
    else:
        return render_template("error.html", message="Viestin poistaminen ei onnistunut")

@app.route("/edit_message", methods=["GET", "POST"])
def edit_message():
    if request.method == "POST" and "content" in request.form:
        content = request.form["content"]
        user_id = request.form["user_id"]
        category = request.form["category"]
        topic = request.form["topic"]
        message_id = request.form["message_id"]
        return render_template("edit.html", content=content, user_id=user_id, category=category, topic=topic, message_id=message_id)
    elif request.method == "POST" and "edited_content" in request.form:
        message_id = request.form["message_id"]
        edited_content = request.form["edited_content"]
        user_id = users.get_user_id()
        category = request.form["category"]
        topic = request.form["topic"]
        if users.session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if threads.edit_message(message_id, edited_content, user_id):
            return redirect(url_for("messages", category=category, topic=topic))
    else:
        return render_template("error.html", message="Viestin muokkaaminen ei onnistunut")

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    if query == "":
        return redirect(request.args["curr_address"])
    messages = threads.search_messages(query)
    return render_template("result.html", messages=messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti epäonnistui")