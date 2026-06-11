import db

def get_all_algorithms():
    sql = """SELECT id, name FROM algorithms"""
    return db.query(sql)

def get_algorithm(algo_id):
    sql = "SELECT id, name, source_code, username FROM algorithms WHERE id = ?"
    result = db.query(sql, [algo_id])
    return result[0] if result else None

def add_algorithm(name, source_code, username, classes):
    sql = """INSERT INTO algorithms (name, source_code, username) VALUES (?, ?, ?)"""
    db.execute(sql, [name, source_code, username])
    algo_id = db.last_insert_id()

    sql = "INSERT INTO algorithm_classes (algo_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [algo_id, title, value])
    return algo_id

def get_classes(algo_id):
    sql = "SELECT title, value FROM algorithm_classes WHERE algo_id = ?"
    return db.query(sql, [algo_id])
    
def remove_algorithm(algo_id):
    sql = "DELETE FROM algorithm_classes WHERE algo_id = ?"
    db.execute(sql, [algo_id])

    sql = "DELETE FROM algorithms WHERE id = ?"
    db.execute(sql, [algo_id])

def update_algorithm(algo_id, name, source_code, username):
    sql = "UPDATE algorithms SET name = ?, source_code = ?, username = ? WHERE id = ?"
    db.execute(sql, [name, source_code, username, algo_id])

def search_algorithms(query):
    sql = "SELECT id, name, source_code, username FROM algorithms WHERE name LIKE ? or source_code LIKE ?"
    query_str = "%" + query + "%"
    return db.query(sql, [query_str, query_str])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql, )

    classes = {}
    for title, value in result:
        classes[title] = []

    for title, value in result:
        classes[title].append(value)

    return classes

def add_benchmark(user_id, algo_id, name, execution_time, metadata):
    sql = """INSERT INTO benchmarks
             (name, execution_time, metadata, sent_at, user_id, algo_id)
             VALUES (?, ?, ?, datetime('now'), ?, ?)"""
    db.execute(sql, [name, execution_time, metadata, user_id, algo_id])

def get_benchmarks_for_algo(algo_id):
    sql = "SELECT name, execution_time, metadata, sent_at, user_id FROM benchmarks WHERE algo_id = ?"
    result = db.query(sql, [algo_id])
    return result if result else None
