from db import db
import users

def show_thread(id):
    sql = "SELECT H.title, H.op_content, (SELECT U.username FROM users U WHERE U.id = H.user_id), R.id, R.content, R.user_id, (SELECT U.username FROM users U WHERE U.id = R.user_id), R.sent_at, H.id, H.user_id FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.id=:id"
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

def delete_reply(id):
     sql = "DELETE FROM replys WHERE id=:id"
     db.session.execute(sql, {"id":id})
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
    
def edit_reply(content, reply_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE replys SET content=:content WHERE id=:reply_id"
    db.session.execute(sql, {"content":content, "reply_id":reply_id})
    db.session.commit()
    return True
    
def delete_thread(id):
    sql = "DELETE FROM threads WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def edit_thread(title, op_content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE threads SET title=:title, op_content=:op_content WHERE id=:thread_id"
    db.session.execute(sql, {"title":title, "op_content":op_content, "thread_id":thread_id})
    db.session.commit()
    return True

def search(query):
    sql = "SELECT R.id, R.content, H.title, (SELECT T.name FROM topics T LEFT JOIN threads J ON J.topic_id = T.id WHERE J.id = H.id), (SELECT U.username FROM users U LEFT JOIN replys D ON U.id = D.user_id WHERE D.id = R.id), H.id FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE R.content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()
     
     
     
     
     
     
