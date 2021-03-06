from flask import session
from db import db


def get_topics():
    sql = """SELECT A.id, A.name,
             (SELECT COUNT(H.*) FROM topics B LEFT JOIN threads H
             ON B.id = H.topic_id WHERE B.id = A.id),
             (SELECT COUNT(R.*) FROM threads H LEFT JOIN replies R
             ON H.id = R.thread_id WHERE H.topic_id = A.id),
             (SELECT MIN(R.sent_at) FROM threads H LEFT JOIN replies R
             ON H.id = R.thread_id WHERE H.topic_id = A.id), A.secret
             FROM topics A WHERE secret=0 ORDER BY A.id"""
    result = db.session.execute(sql)
    return list(result.fetchall())


def get_secret_topics():
    sql = """SELECT A.id, A.name,
             (SELECT COUNT(H.*) FROM topics B LEFT JOIN threads H
             ON B.id = H.topic_id WHERE B.id = A.id),
             (SELECT COUNT(R.*) FROM threads H LEFT JOIN replies R
             ON H.id = R.thread_id WHERE H.topic_id = A.id),
             (SELECT MIN(R.sent_at) FROM threads H LEFT JOIN replies R
             ON H.id = R.thread_id WHERE H.topic_id = A.id),
             A.user_id, A.secret FROM topics A WHERE secret=1 ORDER BY A.id"""
    result = db.session.execute(sql)
    return list(result.fetchall())


def show_topic(id):
    sql = """SELECT T.name, H.id, H.title, H.sent_at, H.user_id, T.secret
             FROM topics T LEFT JOIN threads H  ON T.id = H.topic_id WHERE T.id=:id ORDER BY T.id"""
    result = db.session.execute(sql, {"id": id})
    return list(result.fetchall())


def delete_topic(name):
    basic_topics = ["Jutustelu", "Syvälliset", "Kaveriseuraa", "Apuja"]
    if name in basic_topics:
        return False
    sql = "DELETE FROM topics WHERE name=:name"
    db.session.execute(sql, {"name": name})
    db.session.commit()
    return True


def create_topic(name):
    try:
        sql = "INSERT INTO topics (name, secret) VALUES (:name, 0) RETURNING id"
        new = db.session.execute(sql, {"name": name}).fetchone()[0]
        db.session.commit()
    except:
        return False, False
    return True, new


def create_secret_topic(name, choises):
    try:
        user_id = session.get("user_id", 0)
        sql = "INSERT INTO topics (name, secret, user_id) VALUES (:name, 1, :user_id) RETURNING id"
        new = db.session.execute(
            sql, {"name": name, "user_id": user_id}).fetchone()[0]
        for line in choises.split("\n"):
            line = line.replace("\r", "")

            sql = """INSERT INTO secret (topic_id, user_id)
                     VALUES (:topic_id, (SELECT id  FROM users WHERE username=:line))"""
            db.session.execute(sql, {"topic_id": new, "line": line})

        sql = "INSERT INTO secret (topic_id, user_id) VALUES (:topic_id, :user_id)"
        db.session.execute(sql, {"topic_id": new, "user_id": user_id})

        db.session.commit()
    except:
        return False, False
    return True, new


def get_info_thread(id):
    sql = """SELECT T.name, T.secret, T.id
             FROM topics T LEFT JOIN threads H ON T.id=H.topic_id WHERE H.id=:id"""
    result = db.session.execute(sql, {"id": id})
    return list(result.fetchall())


def get_info_topic(id):
    sql = "SELECT name, secret, id FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_list():
    sql = "SELECT name, id, secret FROM topics ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()


def get_secret(id):
    sql = "SELECT secret FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()[0]
