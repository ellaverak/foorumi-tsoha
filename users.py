from logging import raiseExceptions
import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def register(username, password):
    hash_value = generate_password_hash(password)
    test = []
    for i in get_users():
        test.append(i[1])
    if username in test:
        return False
    try:
        sql = """INSERT INTO users (username,password, role)
                VALUES (:username,:password, 0) RETURNING id"""
        db.session.execute(
            sql, {"username": username, "password": hash_value}).fetchone()
        db.session.commit()
    except:
        return False
    return login(username, password)


def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_role"] = user.role
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False


def logout():
    del session["user_id"]
    del session["user_role"]
    del session["username"]
    del session["csrf_token"]


def get_users():
    sql = "SELECT id, username FROM users ORDER BY username"
    result = db.session.execute(sql)
    return result.fetchall()


def get_secret_users(id):
    sql = """SELECT U.username FROM users U LEFT JOIN secret S ON U.id = S.user_id
              WHERE S.topic_id=:id ORDER BY U.username"""
    result = db.session.execute(sql, {"id": id})
    return list(result.fetchall())


def access(id):
    sql = "SELECT user_id FROM secret WHERE topic_id=:id"
    result = db.session.execute(sql, {"id": id})
    users = list(result.fetchall())
    if session.get("user_role", 0) == 1:
        return True
    for user in users:
        if session.get("user_id", 0) == user[0]:
            return True

    return False


def add_secret(id, choises):
    users = list(get_users())
    for i in range(0, len(users)):
        users[i] = users[i][1]
    print(users)
    try:
        for line in choises.split("\n"):
            line = line.replace("\r", "")
            if line not in users:
                return False

            sql = """INSERT INTO secret (topic_id, user_id)
                     VALUES (:id, (SELECT id  FROM users WHERE username=:line))"""
            db.session.execute(sql, {"id": id, "line": line})

        db.session.commit()
    except:
        return False

    return True
