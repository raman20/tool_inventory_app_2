from flask import Flask,redirect,request,render_template,session,url_for

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>this is home</h1>"

@app.route("/register")
def register():
    pass

@app.route("/login")
def login():
    pass

@app.route("/logout")
def logout():
    pass

app.run()