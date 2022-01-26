import os
from db import db

def get_amount():
    sql = "SELECT H.topic_id, COUNT(R.*) FROM threads H LEFT JOIN Replys R ON R.thread_id = H.id GROUP BY H.topic_id ORDER BY H.topic_id ASC"
    result = db.session.execute(sql)
    return  result.fetchall()
    
def get_time():
    sql = "SELECT H.topic_id, MIN(R.sent_at) FROM threads H LEFT JOIN replys R ON H.id = R.thread_id GROUP BY H.topic_id ORDER BY H.topic_id ASC"
    result = db.session.execute(sql)
    return  result.fetchall()
