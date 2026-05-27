import db

def get_algorithms():
    sql = """SELECT * FROM algorithms"""
    return db.query(sql)

def get_algorithm(algo_id):
    sql = "SELECT * FROM algorithms WHERE id = ?"
    return db.query(sql, [algo_id])

def add_algorithm(name, source_code, username):
    sql = """INSERT INTO algorithms (name, source_code, username) VALUES (?, ?, ?)"""
    db.execute(sql, [name, source_code, username])
    return db.last_insert_id()
    
def remove_algorithm(algo_id):
    sql = "DELETE FROM algorithms WHERE id = ?"
    db.execute(sql, [algo_id])

def update_algorithm(algo_id, name, source_code, username):
    sql = "UPDATE algorithms SET name = ?, source_code = ?, username = ? WHERE id = ?"
    db.execute(sql, [name, source_code, username, algo_id])

def search_algorithms(query):
    sql = "SELECT * FROM algorithms WHERE name LIKE ? or source_code LIKE ?"
    query_str = "%" + query + "%"
    return db.query(sql, [query_str, query_str])