from flask import Flask,redirect,request,render_template,session,url_for,flash,g
from werkzeug.security import check_password_hash,generate_password_hash
from main import create_user,check_login,get_user,add_new_tool,get_projects,create_new_project,get_project_info,get_tool_info,get_tools,complete_project

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
        project=list()
        if user["database"]:
            for i in get_projects(user["database"]):
                project.append([i["_id"],i["proj_name"]])
        return render_template("user.html",name=user["name"],username=user["username"],database=user["database"],admin=user["admin"],project=project)
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
        return redirect(url_for('user',username=session["user"]))

@app.route("/new_project",methods=["POST"])
def new_project():
    if request.method=="POST":
        project_name = request.form["p_name"]
        project_city = request.form["p_city"]
        create_new_project(get_user(session.get("user"))["database"],project_name,project_city)
        return redirect(url_for('user',username=session.get("user")))

@app.route("/project/<int:pid>",methods=["GET","POST"])
def projects(pid):
    project = get_project_info(get_user(session.get("user"))["database"],pid)
    name = project["proj_name"]
    city = project["city"]
    status = project["status"]
    tools = list()
    if project.get("avl"):
        for i in project.get("avl").keys():
            t_name = get_tool_info(get_user(session.get("user"))["database"],int(i))["tool"]
            for quant,sr,date,sender in zip(*project["avl"][i].values()): 
                tools.append([int(i),t_name,quant,sr,date,sender])
    else:
        tools=None
    return render_template("project.html",name=name,pid=pid,city=city,status=status,tools=tools)
        

@app.route("/tool/",methods=["GET","POST"])
@app.route("/tool/<int:tid>",methods=["GET","POST"])
def tools(tid=None):
    if tid:
        tool = get_tool_info(get_user(session["user"])["database"],tid)
        avl = [[i,j] for i,j in zip(*tool["avl"].values())] 
        return render_template("tool.html",tool_id=tid,tool_name=tool['tool'],tool_sr=tool['sr_num'],total_quant=tool['total_quant'],avl=avl)
    else:
        tool = get_tools(get_user(session["user"])["database"])
        tool = [[i['_id'],i['tool'],i['sr_num']] for i in tool]
        return render_template("tool.html",tool=tool)

@app.route("/create_user")
def create_new_user():
    pass

@app.route("/delete/<int:pid>",methods=["GET","POST"])
def delete(pid):
    complete_project(get_user(session["user"])["database"],pid)
    return redirect(url_for('user',username=session['user']))

@app.route("/dispatch")
def dispatch():
    pass

@app.route("/history")
def history():
    pass

app.run(debug=True)