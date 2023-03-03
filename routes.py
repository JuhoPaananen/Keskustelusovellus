"""Module responsible of routing"""

from app import app
from flask import render_template, redirect, request, url_for, abort, flash
import users, forum

@app.route("/")
def index():
    category_list = forum.get_categories()
    return render_template("index.html", categories=category_list)

@app.route("/<string:category>")
def topics(category):
    category_id = forum.get_category_id(category)
    topic_list = forum.get_topics(category_id)
    return render_template("topic.html", topics=topic_list, category=category)

@app.route("/<string:category>/<int:topic>")
def messages(category, topic):
    messages = forum.get_messages(topic, users.get_user_id())
    topic_title = forum.get_topic(topic)
    if forum.topic_is_visible(topic):
        return render_template("messages.html", messages=messages, topic=topic_title, category=category)
    else:
        return render_template("error.html", message="Tämä keskustelu on poistettu")

@app.route("/new_topic", methods=["GET", "POST"])
def new_topic():
    if request.method == "GET":
        category = request.args["category"]
        return render_template("new_topic.html", category=category)
    if request.method == "POST":
        new_topic = request.form["new_topic"]
        category = request.form["category"]
        content = request.form["content"]
        category_id = forum.get_category_id(category)
        if len(new_topic) > 100:
            return render_template("error.html", message="Aihe on liian pitkä")
        if len(content) > 5000:
            return render_template("error.html", message="Viesti on liian pitkä")
        if users.session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if forum.save_new_topic(category_id, new_topic, content, users.get_user_id()):
            new_topic_id = forum.get_topic_id(new_topic)
            return redirect(url_for("messages", category=category, topic=new_topic_id))
        else:
            return render_template("error.html", message="Uuden aiheen luonti ei onnistunut") 
        
@app.route("/remove_topic", methods=["POST"])
def remove_topic():
    topic_id = request.form["topic_id"]
    category = request.form["category"]
    if users.session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if forum.remove_topic(topic_id, users.get_user_id()):
        return redirect(url_for("topics", category=category))
    else:
        return render_template("error.html", message="Keskustelun poistaminen ei onnistunut")

@app.route("/edit_topic", methods=["GET", "POST"])
def edit_topic():
    if request.method == "POST" and "title" in request.form:
        user_id = request.form["user_id"]
        category = request.form["category"]
        title = request.form["title"]
        topic_id = request.form["topic_id"]
        return render_template("edit_topic.html", title=title, user_id=user_id, category=category, topic_id=topic_id)
    if request.method == "POST" and "edited_title" in request.form:
        topic_id = request.form["topic_id"]
        edited_title = request.form["edited_title"]
        user_id = users.get_user_id()
        category = request.form["category"]
        if len(edited_title) > 100:
            return render_template("error.html", message="Aihe on liian pitkä")
        if users.session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if forum.edit_topic(topic_id, edited_title, user_id):
            return redirect(url_for("topics", category=category))
    else:
        return render_template("error.html", message="Otsikon muokkaaminen ei onnistunut")

@app.route("/<string:category>/<string:topic>/<int:message_id>/<int:user_id>/like")
def upvote(category, topic, message_id, user_id):
    topic_id = forum.get_topic_id(topic)
    if forum.like(message_id, user_id):
        return redirect(url_for("messages", category=category, topic=topic_id))
    else:
        return render_template("error.html", message="Tykkääminen ei onnistunut")

@app.route("/<string:category>/<string:topic>/<int:message_id>/<int:user_id>/unlike")
def downvote(category, topic, message_id, user_id):
    topic_id = forum.get_topic_id(topic)
    if forum.unlike(message_id, user_id):
        return redirect(url_for("messages", category=category, topic=topic_id))
    else:
        return render_template("error.html", message="Tykkäämisen poistaminen ei onnistunut")

@app.route("/add", methods=["POST"])
def add_message():
    topic = request.form["topic"]
    category = request.form["category"]
    content = request.form["content"]
    topic_id = forum.get_topic_id(topic)
    if len(content) > 5000:
            return render_template("error.html", message="Viesti on liian pitkä")
    if users.session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if forum.save_new_message(content, topic_id, users.get_user_id()):
        return redirect(url_for("messages", category=category, topic=topic_id))
    else: 
        return render_template("error.html", message="Viestin lähettäminen ei onnistunut")

@app.route("/remove_message", methods=["POST"])
def remove_message():
    message_id = request.form["message_id"]
    topic = request.form["topic"]
    topic_id = forum.get_topic_id(topic)
    category = request.form["category"]
    if users.session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if forum.remove_message(message_id, users.get_user_id()):
        return redirect(url_for("messages", category=category, topic=topic_id))
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
        topic_id = forum.get_topic_id(topic)
        if len(edited_content) > 5000:
            return render_template("error.html", message="Viesti on liian pitkä")
        if users.session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if forum.edit_message(message_id, edited_content, user_id):
            return redirect(url_for("messages", category=category, topic=topic_id))
    else:
        return render_template("error.html", message="Viestin muokkaaminen ei onnistunut")

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    if query == "":
        return redirect("/")
    messages = forum.search_messages(query)
    return render_template("result.html", messages=messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            flash("Kirjautuminen onnistui")
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    flash("Olet kirjautunut ulos")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) > 50:
            return render_template("error.html", message="Käyttäjätunnus on yli 50 merkkiä")
        if len(password1) > 100:
            return render_template("error.html", message="Salasana on yli 100 merkkiä pitkä")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if users.register(username, password1):
            flash("Rekisteröityminen onnistui, olet kirjautunut sisään")
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti epäonnistui")