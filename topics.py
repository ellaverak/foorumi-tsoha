from db import db

def get_topics():
    sql = "SELECT id, name FROM topics ORDER BY id DESC"
    result = db.session.execute(sql)
    return  result.fetchall()

def show_topic(id):
    sql = "SELECT name FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    return topic
