from db import db
import users

def show_thread(id):
    sql = "SELECT H.title, H.op_content, R.id, R.content, R.user_id, (SELECT U.username FROM users U WHERE U.id = R.user_id), R.sent_at FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.id=:id"
    result = db.session.execute(sql, {"id":id})
    return  result.fetchall()

def create_thread(title, op_content, topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO threads (title, op_content, topic_id, user_id, sent_at) VALUES (:title, :op_content, :topic_id, :user_id, NOW())"
    db.session.execute(sql, {"title":title, "op_content":op_content, "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

def reply(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO replys (content, thread_id, user_id, sent_at) VALUES (:content, :thread_id, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True
    
 
