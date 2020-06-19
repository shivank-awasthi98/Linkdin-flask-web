from application import app
from flask import render_template

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",login=False)
@app.route("/login")
def login():
    return render_template("login.html",login=False)
@app.route("/cources")
def cources():
    return render_template("cources.html",login=False)
@app.route("/register")
def register():
    return render_template("register.html",login=False)