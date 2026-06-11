import sqlite3
from flask import Flask, render_template, request, redirect, session, abort, flash
import markupsafe
import secrets
import db
import config
import algorithms
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    algos = algorithms.get_all_algorithms()
    return render_template("index.html", algos=algos)

@app.route("/new_algorithm", methods=["GET", "POST"])
def new_algorithm():
    all_classes = algorithms.get_all_classes()

    if request.method == "GET":
        return render_template("new_algorithm.html", all_classes=all_classes)
    
    if request.method == "POST":
        check_csrf()
        algo_name = request.form["algo_name"]
        source_code = request.form["source_code"]
        input_classes = request.form.getlist("classes")
        print(input_classes)
        classes = []
        if input_classes:
            for entry in input_classes:
                splitted = entry.split(":")
                classes.append((splitted[0], splitted[1]))
        print(classes)
        username = session["username"]
        if not algo_name or len(algo_name) > 100 or len(source_code) > 10000:
            abort(403)
        algo_id = algorithms.add_algorithm(algo_name, source_code, username, classes)
        return redirect("/algorithm/" + str(algo_id))

@app.route("/algorithm/<int:algo_id>")
def show_algorithm(algo_id):
    algo = algorithms.get_algorithm(algo_id)
    classes = algorithms.get_classes(algo_id)
    benchmarks = algorithms.get_benchmarks_for_algo(algo_id)
    if not algo:
        abort(404)
    return render_template("algorithm.html", algo=algo, classes=classes, benchmarks=benchmarks)

@app.route("/remove/<int:algo_id>", methods=["GET", "POST"])
def remove(algo_id):

    algo = algorithms.get_algorithm(algo_id)

    if not algo:
        abort(404)

    if algo["username"] != session.get("username"):
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", algo_id=algo_id)
    
    if request.method == "POST":
        check_csrf()
        algorithms.remove_algorithm(algo_id)
        return redirect("/")
    
@app.route("/new_benchmark", methods=["POST"])
def new_benchmark():

    if request.method == "POST":
        check_csrf()
        benchmark_name = request.form["benchmark_name"]
        execution_time = request.form["execution_time"]
        execution_time = validate_float(execution_time)
        metadata = request.form["metadata"]
        username = session["username"]
        user_id = users.get_user_id(username)[0]
        algo_id = int(request.form["algo_id"])

        print(type(user_id))

        if not execution_time or len(benchmark_name) > 100 or len(metadata) > 1000:
            abort(403)
        try:
            algorithms.add_benchmark(user_id, algo_id, benchmark_name, execution_time, metadata)
        except sqlite3.IntegrityError:
            abort(403)
        return redirect("/algorithm/" + str(algo_id))

@app.route("/cancel/<int:algo_id>", methods=["POST"])
def cancel(algo_id):
    return redirect("/algorithm/" + str(algo_id))

@app.route("/edit/<int:algo_id>", methods=["GET", "POST"])
def edit_algorithm(algo_id):
    algo = algorithms.get_algorithm(algo_id)

    if not algo:
        abort(404)

    if algo["username"] != session.get("username"):
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", algo=algo)
    
    if request.method == "POST":
        check_csrf()
        algo_name = request.form["name"]
        source_code = request.form["source_code"]
        if not algo_name or len(algo_name) > 100 or len(source_code) > 10000:
            abort(403)
        algorithms.update_algorithm(algo["id"], algo_name, source_code, session["username"])
        return redirect("/algorithm/" + str(algo["id"]))
    
@app.route("/search")
def search():
    query = request.args.get("query")
    results = algorithms.search_algorithms(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/user/<string:username>")
def show_user(username):
    #username = users.get_user(user_id)[0]
    user_id = users.get_user_id(username)[0]
    algos = users.get_algorithms_by_user(username)
    benchmarks = users.get_benchmarks_by_user(user_id)
    return render_template("user.html", username=username, algos=algos, benchmarks=benchmarks)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        if session.get("username"):
            return redirect("/")  # redirect to / if logged in
        else:
            return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.check_login(username, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä käyttäjätunnus tai salasana")
            return redirect("/login")
    
@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: salasanat eivät täsmänneet")
            return redirect("/register")
        

        try:
            users.create_user(username, password1)
        except sqlite3.IntegrityError:
            flash("VIRHE: käyttäjätunnus on jo varattu")
            return redirect("/register")
        
        flash("Tunnus luotu!")
        return redirect("/")

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    
def validate_float(input):
    try:
        return float(input)
    except ValueError:
        abort(403)

    

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    content = content.replace(" ", "&nbsp;")
    return markupsafe.Markup(f"<pre>{content}</pre>")