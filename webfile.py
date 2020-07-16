from flask import Flask,redirect,request,render_template,session,url_for,flash,g
from werkzeug.security import check_password_hash,generate_password_hash
from main import create_user,check_login,get_user,add_new_tool

app = Flask(__name__)
app.secret_key=b"!@#$!@#$!@#$1234"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form['name']
        error = create_user(name,username,generate_password_hash(password))
        if error is None:
            return redirect(url_for("login"))
        else:
            return render_template("register.html",error=error)
    return render_template("register.html",error=None)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        result = check_login(username)
        if result:
            if check_password_hash(result,password):
                session['user'] = username
                return redirect(url_for('user',username=username))
        else:
            error = 'username or password is wrong'
            return render_template("login.html",error=error)
    return render_template("login.html",error=None)

@app.route("/user/<username>",methods=["GET","POST"])
def user(username):
    user=get_user(username)
    if session.get("user",None) == username:
        return render_template("user.html",name=user["name"],username=user["username"],database=user["database"],admin=user["admin"])
    else:
        return redirect(url_for("login"))

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))

@app.route("/add_new_tools",methods=["POST"])
def new_tool():
    if request.method == "POST":
        tool_name=request.form["tool_name"]
        tool_quant=request.form["tool_quant"]
        tool_sr = request.form["tool_sr"]
        db_name = get_user(session.get("user",None))["database"]
        add_new_tool(db_name,tool_name,tool_quant,tool_sr)

app.run(debug=True)