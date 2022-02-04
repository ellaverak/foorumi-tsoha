import os
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, role) VALUES (:username,:password, 0)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)
    
def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_role"] = user.role
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_role"]

def user_id():
    return session.get("user_id",0)
    
def require_role(role):
    return session.get("user_role", 0)
    
def get_users():
    sql = "SELECT id, username FROM users ORDER BY username ASC"
    result = db.session.execute(sql)
    return result.fetchall()

def access(id):
    sql = "SELECT user_id FROM secret WHERE topic_id=:id"
    result = db.session.execute(sql, {"id":id})
    users = list(result.fetchall())
    user_id = session.get("user_id",0)
    for user in users:
        if user_id == user[0]:
            return True
    
    return False
