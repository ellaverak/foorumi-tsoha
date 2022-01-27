from db import db

def get_topics():
    sql = "SELECT A.id, A.name, (SELECT COUNT(H.*) FROM topics B LEFT JOIN threads H ON B.id = H.topic_id WHERE B.id = A.id), (SELECT COUNT(R.*) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.topic_id = A.id), (SELECT MIN(R.sent_at) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.topic_id = A.id) FROM topics A"
    result = db.session.execute(sql)
    return  result.fetchall()

def show_topic(id):
    sql = "SELECT T.name, H.id, H.title FROM topics T LEFT JOIN threads H  ON T.id = H.topic_id WHERE T.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()
