from db import db
import users
import textwrap
from flask import session

def leave_reply(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
        
    content = "\n".join(textwrap.wrap(content, width=78))
    
    sql = "INSERT INTO replies (content, thread_id, user_id, sent_at) VALUES (:content, :thread_id, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()
    return True
    
def edit_reply(content, reply_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    content = "\n".join(textwrap.wrap(content, width=78))
    
    sql = "UPDATE replies SET content=:content WHERE id=:reply_id"
    db.session.execute(sql, {"content":content, "reply_id":reply_id})
    db.session.commit()
    return True

def delete_reply(id):
     try:
         sql = "DELETE FROM replies WHERE id=:id RETURNING thread_id"
         thread_id = db.session.execute(sql, {"id":id}).fetchone()[0]
         db.session.commit()
     except:
         return False, False
     return True, thread_id
    
def search(query):
    sql = """SELECT R.id, R.content, H.title, 
             (SELECT T.name FROM topics T LEFT JOIN threads J ON J.topic_id = T.id WHERE J.id = H.id), 
             (SELECT U.username FROM users U LEFT JOIN replies D ON U.id = D.user_id WHERE D.id = R.id), 
             (SELECT T.secret FROM topics T LEFT JOIN threads J ON J.topic_id = T.id WHERE J.id = H.id), 
             H.id FROM threads H LEFT JOIN replies R ON H.id = R.thread_id WHERE lOWER(R.content) LIKE LOWER(:query)"""
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()
