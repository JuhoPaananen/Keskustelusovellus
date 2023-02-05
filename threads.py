from db import db
from sqlalchemy.sql import text

def get_categories():
    # add checks for hidden categories
    sql = text("SELECT * FROM categories")
    result = db.session.execute(sql)
    return result.fetchall()

def get_category_id(category_name):
    sql = text("SELECT id FROM categories WHERE name = :category_name")
    result = db.session.execute(sql, {'category_name':category_name})
    return result.fetchone()[0]

def get_topic_id(topic_name):
    sql = text("SELECT id FROM topics WHERE title = :topic_name")
    result = db.session.execute(sql, {'topic_name':topic_name})
    return result.fetchone()[0]

def get_topics(id):
    sql = text("SELECT T.title, U.username, T.created_at FROM topics T, users U WHERE T.category_id = :category_id")
    result = db.session.execute(sql, {'category_id': id})
    return result.fetchall()

def save_new_message(content, topic_id, user_id):
    sql = text("INSERT INTO messages (user_id, topic_id, content) VALUES (:user_id, :topic_id, :content)")
    db.session.excute(sql, {'user:id':user_id, 'topic_id':topic_id, 'content':content})
    db.session.commit()
    return True


def get_messages(topic_id):
    sql = text("SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.topic_id = :topic_id")
    result = db.session.execute(sql, {'topic_id':topic_id})
    return result.fetchall()

def search_messages(keyword):
    sql = text("SELECT id, user_id, content, sent_at FROM messages WHERE content LIKE :query")
    result = db.session.execute(sql, {"query":"%"+keyword+"%"})
    return result.fetchall()
