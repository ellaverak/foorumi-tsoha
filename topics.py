import os
from db import db

def get_topics():
    sql = "SELECT id, name FROM topics"
    result = db.session.execute(sql)
    return  result.fetchall()

def show_topic(id):
    sql = "SELECT name FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
