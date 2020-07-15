from flask import Flask,redirect,request,render_template,session,url_for,flash,g
from werkzeug.security import check_password_hash,generate_password_hash
from main import create_user

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = create_user(username,generate_password_hash(password))
        if error is None:
            return redirect(url_for("login"))
        flash(error)
    return render_template("register.html")

@app.route("/login")
def login():
    return '<h1>LOGIN</h1>'

@app.route("/logout")
def logout():
    pass

app.run(debug=True)