from db import db
from flask import session

def get_topics():
    sql = "SELECT A.id, A.name, (SELECT COUNT(H.*) FROM topics B LEFT JOIN threads H ON B.id = H.topic_id WHERE B.id = A.id), (SELECT COUNT(R.*) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.topic_id = A.id), (SELECT MIN(R.sent_at) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.topic_id = A.id) FROM topics A WHERE secret=0"
    result = db.session.execute(sql)
    return  result.fetchall()

def get_secret_topics():
    sql = "SELECT A.id, A.name, (SELECT COUNT(H.*) FROM topics B LEFT JOIN threads H ON B.id = H.topic_id WHERE B.id = A.id), (SELECT COUNT(R.*) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.topic_id = A.id), (SELECT MIN(R.sent_at) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.topic_id = A.id) FROM topics A WHERE secret=1"
    result = db.session.execute(sql)
    return  result.fetchall()

def show_topic(id):
    sql = "SELECT T.name, H.id, H.title, H.sent_at, H.user_id FROM topics T LEFT JOIN threads H  ON T.id = H.topic_id WHERE T.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()
    
def delete_topic(name):
    sql = "DELETE FROM topics WHERE name=:name"
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return True

def create_topic(name):
    sql = "INSERT INTO topics (name, secret) VALUES (:name, 0)"
    db.session.execute(sql, {"name":name})
    db.session.commit()
    return True

def create_secret_topic(name, choises):
    sql = "INSERT INTO topics (name, secret) VALUES (:name, 1)"
    db.session.execute(sql, {"name":name})
    sql = "SELECT id FROM topics WHERE name=:name"
    topic_id = db.session.execute(sql, {"name":name}).fetchone()[0]
    user_id = session.get("user_id", 0)
    for line in choises.split("\n"):
        
        sql = "INSERT INTO secret (topic_id, user_id) VALUES (:topic_id, (SELECT id  FROM users WHERE username=:line))"
        db.session.execute(sql, {"topic_id":topic_id, "line":line})
    
    sql = "INSERT INTO secret (topic_id, user_id) VALUES (:topic_id, :user_id)"
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    
    db.session.commit()
    return True
