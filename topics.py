from db import db

def get_topics():
    sql = "SELECT name FROM topics"
    result = db.session.execute(sql)
    topics = result.fetchall()
    return topics
