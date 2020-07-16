# mongoDB python client
import pymongo
import datetime

# connecting to mongoDB
def connect_db(db_name):
    db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = db[db_name]
    db.close()
    return mydb

db = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = db["testdb"]
main = mydb["main"]
projects = mydb["projects"]
dispatch = mydb["dispatch"]
history = mydb['history']

day = datetime.datetime.now().day
month = datetime.datetime.now().month
year = datetime.datetime.now().year


def get_tools():
    return main.find()

def get_tool_info(tool_id):
    return main.find_one({"_id":tool_id})


def add_tool(tool_id,quantity,project_id,sender=None):
    if sender:
        project_info = get_project_info(sender)
        tool_info = project_info["avl"][str(tool_id)]
        tool_quant = tool_info["quant"]
        tool_sr = tool_info["sr"]
        tool_from = tool_info['from']
        tool_sender = tool_info['sender']
        if quantity <= sum(tool_quant):
            if quantity == sum(tool_quant):
                projects.update_one({"_id":project_id},
                {
                    "$push":{
                        f"avl.{tool_id}.quant":{"$each":tool_quant},
                        f"avl.{tool_id}.sr":{"$each":tool_sr},
                        f"avl.{tool_id}.from":{"$each":[f'{day}/{month}/{year}']*len(tool_quant)},
                        f"avl.{tool_id}.sender":{"$each":[sender]*len(tool_quant)}
                    }
                },upsert=True)
                projects.update_one({"_id":sender},
                {
                    "$unset":{
                        f"avl.{tool_id}":''
                    }
                })
                #creating history
                for i in range(len(tool_quant)):
                    history.insert_one({
                        "_id":history.count()+1,
                        "tool_id":tool_id,
                        "quant":tool_quant[i],
                        "sr":tool_sr[i],
                        'from':tool_from[i],
                        'till':f'{day}/{month}/{year}',
                        'sender':tool_sender[i],
                        "recv":project_id
                        })
                main.update_one({"_id":tool_id},{"$pull":{"pid":sender}})
            else:
                for i in range(len(tool_quant)):
                    if quantity < tool_quant[i]:
                        sr = tool_sr[i]
                        projects.update_one({"_id":project_id},
                        {
                            "$push":{
                                f"avl.{tool_id}.quant":quantity,
                                f"avl.{tool_id}.sr":sr,
                                f"avl.{tool_id}.from":f"{day}/{month}/{year}",
                                f"avl.{tool_id}.sender":sender
                            }
                        },upsert=True)
                        history.insert_one({
                            "_id":history.count()+1,
                            "tool_id":tool_id,
                            "quant":tool_quant,
                            "sr":tool_sr[i],
                            "from":tool_from[i],
                            "till":f'{day}/{month}/{year}',
                            "sender":tool_sender[i],
                            "recv":sender
                            })
                        projects.update_one({"_id":sender},
                        {
                            "$set":{
                                f"avl.{tool_id}.quant.{i}":tool_quant[i]-quantity,
                                f'avl.{tool_id}.sr.{i}':tool_sr[i].split("_")[0]+"_"+str(int(tool_sr[i].split("_")[1])+quantity),
                                f"avl.{tool_id}.from.{i}":f"{day}/{month}/{year}"
                            }
                        })
                    else:
                        quantity -= tool_quant[i]
                        sr = tool_sr[i]
                        projects.update_one({"_id":project_id},
                        {
                            "$push":{
                                f"avl.{tool_id}.quant":tool_quant[i],
                                f"avl.{tool_id}.sr":sr,
                                f"avl.{tool_id}.from":f"{day}/{month}/{year}",
                                f"avl.{tool_id}.sender":sender
                            }
                        },upsert=True)
                        history.insert_one({
                            "_id":history.count()+1,
                            "tool_id":tool_id,
                            "quant":tool_quant[i],
                            "sr":sr,
                            "from":tool_from[i],
                            "till":f"{day}/{month}/{year}",
                            "sender":tool_sender[i],
                            "recv":sender
                            })
                        projects.update_one({"_id":sender},
                        {
                            "$set":{
                                f"avl.{tool_id}.quant.{i}":0,
                                f'avl.{tool_id}.sr.{i}':0,
                                f"avl.{tool_id}.from.{i}":0,
                                f"avl.{tool_id}.sender.{i}":0
                            }
                        })
                projects.update_one({"_id":sender},
                        {
                            "$pull":{
                                f"avl.{tool_id}.quant":0,
                                f'avl.{tool_id}.sr':0,
                                f"avl.{tool_id}.from":0,
                                f"avl.{tool_id}.sender":0
                            }
                        })
                        
        else:
            print("insufficient quantity")    

    else:
        tool_info = get_tool_info(tool_id)
        tool_quant = tool_info['avl']['quant']
        tool_sr = tool_info['avl']['sr']
        if quantity <= sum(tool_quant):
            if quantity == sum(tool_quant):
                projects.update_one({"_id":project_id},
                {
                    "$push":{
                        f"avl.{tool_id}.quant":{"$each":tool_quant},
                        f"avl.{tool_id}.sr":{"$each":tool_sr},
                        f"avl.{tool_id}.from":{"$each":[f'{day}/{month}/{year}']*len(tool_quant)},
                        f"avl.{tool_id}.sender":{"$each":["main"]*len(tool_quant)}
                    }
                },upsert=True)
                main.update_one({"_id":tool_id},
                {
                    "$set":{
                        "avl.quant":[],
                        "avl.sr":[]
                    }
                })
            else:
                for i in range(len(tool_quant)):
                    if quantity < tool_quant[i]:
                        sr=tool_sr[i]
                        projects.update_one({"_id":project_id},
                        {
                            "$push":{
                                f"avl.{tool_id}.quant":quantity,
                                f"avl.{tool_id}.sr":sr,
                                f"avl.{tool_id}.from":f"{day}/{month}/{year}",
                                f"avl.{tool_id}.sender":"main"
                            }
                        },upsert=True)
                        main.update_one({"_id":tool_id},
                        {
                            "$set":{
                                f"avl.quant.{i}":tool_quant[i]-quantity,
                                f"avl.sr.{i}":tool_sr[i].split("_")[0]+"_"+str(int(tool_sr[i].split("_")[1])+quantity)
                            }
                        })
                        break
                    else:
                        quantity -= tool_quant[i]
                        sr = tool_sr[i]
                        projects.update_one({"_id":project_id},
                        {
                            "$push":{
                                f"avl.{tool_id}.quant":tool_quant[i],
                                f"avl.{tool_id}.sr":sr,
                                f"avl.{tool_id}.from":f"{day}/{month}/{year}",
                                f"avl.{tool_id}.sender":"main"
                            }
                        },upsert=True)
                        main.update_one({"_id":tool_id},
                        {
                            "$set":{
                                f"avl.quant.{i}":0,
                                f"avl.sr.{i}":0
                            }
                        })
                main.update_one({"_id":tool_id},
                {
                    "$pull":{
                        "avl.quant":0,
                        "avl.sr":0
                    }
                })
        else:
            print('insufficient quantity')    

    if project_id not in main.find_one({"_id":tool_id})["pid"]:
                        main.update_one({"_id":tool_id},
                        {
                            "$push":{
                                "pid":project_id
                            }
                        })
    organize_main()

def create_new_project():
    #project details
    project_name = input("enter project name:-> ")
    city = input('select city:-> ')
    projects.insert_one({
            "_id":projects.count()+1,
            'proj_name':project_name,
            'city':city,
            "status":"active"})    

def get_projects():
    for i in projects.find():
        print(i)

def get_project_info(project_id):
    return projects.find_one({"_id":project_id})

def delete_project(project_id):
    pass

def get_history():
    return history.find()

def get_tool_history(tool_id):
    return history.find({"tool_id":tool_id})

def get_project_history(pid):
    return history.find({"pid":pid})

def get_tool_presence(tool_id):
    l=[]
    p = get_tool_info(tool_id)["pid"]
    if p:
        for i in p:
            l.append(get_project_info(i)["avl"][str(tool_id)])
        return l
    else:
        return "nowhere"

def create_dispatch(tools,quantity,sr,sender,recv,):
    for i,j,k in zip(tools,quantity,sr):
        dispatch.insert_one({
            "_id":dispatch.count()+1,
            "tool_id":i,
            "sr":k,
            "quantity":j,
            "sender":sender,
            "recv":recv,
            "date":f"{day}/{month}/{year}"
        })

def add_new_tool():
    pass

def complete_project(pid):
    project = get_project_info(pid)
    tool_id = project["avl"].keys()
    quant = list()
    for i in tool_id:
        quant.append(sum(project["avl"][i]["quant"]))
    for i,j in zip(tool_id,quant):
        add_tool(int(i),j,pid)

def organize_main():
    for i in get_tools():
        quant = i["avl"]["quant"]
        sr = i["avl"]["sr"]
        name=i["tool"]
        d = dict()
        for i in sr:
            d[i] = quant[i]
        d = dict(sorted(d.items(),key=lambda item: item[0][item[0].index("_")+1]))
        sr = d.keys()
        quant =  d.values()
        for i in sr[:-1]:
            if i in sr:
                for j in sr[sr.index(i)+1:]:
                    if name+"_"+str(int(i[i.index("_")+1])+quant[sr.index(i)]) == j:
                        quant[sr.index(i)]+=quant[sr.index(j)]
                        quant.pop(sr.index(j))
                        sr.pop(sr.index(j))
        main.update_one({"_id":i["_id"]},
        {
            "$set":{
                "avl.quant":quant,
                "avl.sr":sr
            }
        })

def create_user(name,username,password):
    db=connect_db("userdb")
    user = db['user']
    if not user.find_one({"username":username}):
        user.insert_one({
            "_id":user.count()+1,
            "name":name,
            "username":username,
            "password":password,
            "admin":1,
            "database":""
            })
    else:
        return 'username exist try again'

def check_login(username):
    db=connect_db("userdb")
    user = db["user"]
    if not user.find_one({"username":username}):
        return False
    else:
        return user.find_one({"username":username})["password"] 

def get_user(username):
    return connect_db("userdb")["user"].find_one({"username":username})

def create_main_list():
    pass