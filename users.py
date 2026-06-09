import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id):
    sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_algorithms_by_user(username):
    sql = "SELECT id, name FROM algorithms WHERE username = ?"
    return db.query(sql, [username])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    
    if not result:
        return False
    
    password_hash = result[0][0]

    if check_password_hash(password_hash, password):
        return True
    else:
        return False