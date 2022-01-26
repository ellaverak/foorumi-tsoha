from db import db

def get_topics():
    sql = "SELECT T.id, T.name, COUNT(H.*) FROM topics T LEFT JOIN threads H ON T.id = H.topic_id GROUP BY T.id ORDER BY T.id ASC"
    result = db.session.execute(sql)
    return  result.fetchall()

def show_topic(id):
    sql = "SELECT name FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]
