"""This module takes care of database methods and functions"""

from db import db
from sqlalchemy.sql import text
import datetime

def get_categories():
    # add checks for hidden categories
    sql = text("SELECT C.name, COUNT(DISTINCT(T.id)), COUNT(M.id) FILTER (WHERE M.visible=TRUE) AS messages_count, MAX(M.sent_at) \
                FROM categories C \
                LEFT JOIN topics T ON C.id = T.category_id \
                LEFT JOIN messages M ON T.id = M.topic_id \
                GROUP BY C.name \
                ORDER BY messages_count DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def get_category_id(category_name):
    sql = text("SELECT id FROM categories WHERE name=:category_name")
    result = db.session.execute(sql, {"category_name":category_name})
    return result.fetchone()[0]

def get_topic_id(topic_name):
    sql = text("SELECT id FROM topics WHERE title = :topic_name")
    result = db.session.execute(sql, {"topic_name":topic_name})
    return result.fetchone()[0]

def get_topics(id):
    sql = text("SELECT T.title, U.username, T.created_at, T.user_id, T.id \
                FROM topics T \
                LEFT JOIN users U ON T.user_id = U.id \
                WHERE T.category_id = :category_id AND T.visible=:visible \
                ORDER BY T.created_at ASC")
    result = db.session.execute(sql, {"category_id": id, "visible":"TRUE"})
    return result.fetchall()

def save_new_message(content, topic_id, user_id):
    sent_at = datetime.datetime.now()
    sql = text("INSERT INTO messages (user_id, topic_id, content, sent_at) \
                VALUES (:user_id, :topic_id, :content, :sent_at)")
    db.session.execute(sql, {"user_id":user_id, "topic_id":topic_id, "content":content, "sent_at":sent_at})
    db.session.commit()
    return True

def remove_message(message_id, user_id):
    updated_at = datetime.datetime.now()
    sql = text("UPDATE messages SET visible=:bool, updated_at=:updated \
                WHERE id=:message_id AND user_id=:user_id")
    db.session.execute(sql, {"bool":"FALSE", "updated":updated_at, "message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True

def get_messages(topic_id):
    sql = text("SELECT M.content, U.username, M.sent_at, U.id, M.id \
                FROM messages M \
                LEFT JOIN users U ON M.user_id = U.id \
                WHERE M.topic_id = :topic_id AND visible=:visible \
                ORDER BY M.sent_at ASC")
    result = db.session.execute(sql, {"topic_id":topic_id, "visible":"TRUE"})
    return result.fetchall()

def search_messages(keyword):
    query = "%"+keyword+"%"
    sql = text("SELECT M.content, M.sent_at, M.id, T.title, C.name \
                FROM messages M \
                LEFT JOIN topics T ON M.topic_id = T.id \
                LEFT JOIN categories C ON T.category_id = C.id \
                WHERE M.content LIKE :query AND M.visible=:visible \
                ORDER BY M.sent_at ASC")
    result = db.session.execute(sql, {"query":query, "visible":"TRUE"})
    return result.fetchall()

def save_new_topic(category_id, new_topic, content, user_id):
    sql_topic = text("INSERT INTO topics (user_id, category_id, title) \
                      VALUES (:user_id, :category_id, :title)")
    db.session.execute(sql_topic, {"user_id":user_id, "category_id":category_id, "title":new_topic})
    db.session.commit()
    new_topic_id = get_topic_id(new_topic)
    save_new_message(content, new_topic_id, user_id)
    return True

def remove_topic(topic_id, user_id):
    sql = text("UPDATE topics SET visible=:bool \
                WHERE id=:topic_id AND user_id=:user_id")
    db.session.execute(sql, {"bool":"FALSE", "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

def edit_topic(topic_id, edited_title, user_id):
    sql = text("UPDATE topics SET title=:title WHERE id=:topic_id AND user_id=:user_id")
    db.session.execute(sql, {"title":edited_title, "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

def edit_message(message_id, content, user_id):
    updated_at = datetime.datetime.now()
    sql = text("UPDATE messages SET content=:content, updated_at=:updated \
                WHERE id=:message_id AND user_id=:user_id")
    db.session.execute(sql, {"content":content, "updated":updated_at, "message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True

def topic_is_visible(topic_id):
    sql = text("SELECT visible FROM topics WHERE id=:topic_id")
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()[0]