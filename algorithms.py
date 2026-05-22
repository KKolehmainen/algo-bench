import db

def get_algorithms():
    sql = """SELECT name FROM algorithms"""
    return db.query(sql)

def get_algorithm(algo_id):
    sql = "SELECT * FROM algorithms WHERE id = ?"
    return db.query(sql, [algo_id])

def add_algorithm(name, source_code, username):
    sql = """INSERT INTO algorithms (name, source_code, username) VALUES (?, ?, ?)"""
    db.execute(sql, [name, source_code, username])
    return db.last_insert_id()
    
