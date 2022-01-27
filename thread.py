import os
from db import db

def show_thread(id):
    sql = "SELECT H.title, H.op_content, R.id, R.content, R.user_id, (SELECT U.username FROM users U WHERE U.id = R.user_id), R.sent_at FROM threads H LEFT JOIN replys R ON H.id = R.thread_id WHERE H.id=:id"
    result = db.session.execute(sql, {"id":id})
    return  result.fetchall()
    

