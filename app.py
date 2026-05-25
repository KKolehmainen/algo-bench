import sqlite3
from flask import Flask, render_template, request, redirect, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import algorithms

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    algos = algorithms.get_algorithms()
    return render_template("index.html", algos=algos)

@app.route("/new_algorithm", methods=["GET", "POST"])
def new_algorithm():
    if request.method == "GET":
        return render_template("new_algorithm.html")
    
    if request.method == "POST":
        algo_name = request.form["algo_name"]
        source_code = request.form["source_code"]
        username = session["username"]
        algo_id = algorithms.add_algorithm(algo_name, source_code, username)  # user id here!!!
        return redirect("/algorithm/" + str(algo_id))

@app.route("/algorithm/<int:algo_id>")
def show_algorithm(algo_id):
    algo = algorithms.get_algorithm(algo_id)[0]  # all rows fetched, pick first
    return render_template("algorithm.html", algo=algo)

@app.route("/remove/<int:algo_id>", methods=["GET", "POST"])
def remove(algo_id):

    algo = algorithms.get_algorithm(algo_id)[0]
    if algo["username"] != session.get("username"):
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", algo_id=algo_id)
    
    if request.method == "POST":
        algorithms.remove_algorithm(algo_id)
        return redirect("/")

@app.route("/cancel/<int:algo_id>", methods=["POST"])
def cancel(algo_id):
    return redirect(f"/algorithm/{algo_id}")


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

        try:
            sql = "SELECT password_hash FROM users WHERE username = ?"
            password_hash = db.query(sql, [username])[0][0]
        except:
            return "VIRHE: väärä käyttäjätunnus tai salasana" 

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä käyttäjätunnus tai salasana"
    
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "VIRHE: salasanat eivät täsmänneet"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: käyttäjätunnus on jo varattu"
    
    return "Tunnus luotu"
