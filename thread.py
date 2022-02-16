from db import db
import users
from flask import session

def show_thread(id):
    sql = "SELECT H.title, H.op_content, (SELECT U.username FROM users U WHERE U.id = H.user_id), R.id, R.content, R.user_id, (SELECT U.username FROM users U WHERE U.id = R.user_id), R.sent_at, H.id, H.user_id FROM threads H LEFT JOIN replies R ON H.id = R.thread_id WHERE H.id=:id"
    result = db.session.execute(sql, {"id":id})
    return  list(result.fetchall())

def create_thread(title, op_content, topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (title, op_content, topic_id, user_id, sent_at) VALUES (:title, :op_content, :topic_id, :user_id, NOW()) RETURNING id"
    new = db.session.execute(sql, {"title":title, "op_content":op_content, "topic_id":topic_id, "user_id":user_id}).fetchone()[0]
    db.session.commit()
    return True, new
    
def delete_thread(id):
    try:
        sql = "DELETE FROM threads WHERE id=:id RETURNING topic_id"
        topic_id = db.session.execute(sql, {"id":id}).fetchone()[0]
        db.session.commit()
    except:
        return False
    return True, topic_id

def edit_thread(title, op_content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE threads SET title=:title, op_content=:op_content WHERE id=:thread_id"
    db.session.execute(sql, {"title":title, "op_content":op_content, "thread_id":thread_id})
    db.session.commit()
    return True
     
     
     
     
     
     
