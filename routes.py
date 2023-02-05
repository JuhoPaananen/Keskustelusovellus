from app import app
from flask import render_template, redirect, request
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
    #category_id = messages.get_category_id(category)
    topic_id = threads.get_topic_id(topic)
    messages = threads.get_messages(topic_id)
    return render_template("messages.html", messages=messages, topic=topic, category=category)

@app.route("/new", methods=["POST"])
def send():
    topic = request.form["topic"]
    category = request.form["category"]
    topic_id = threads.get_topic_id(request.form["topic"])
    new_message = request.form["message"]
    threads.save_new_message(new_message, topic_id, users.user_id())
    return redirect("/")

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
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
'''
app.route("/new_topic")
def new_topic():


@app.route("/new_message")
def new_message():
'''