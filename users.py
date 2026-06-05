import db

def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_algorithms_by_user(username):
    sql = "SELECT id, name FROM algorithms WHERE username = ?"
    return db.query(sql, [username])