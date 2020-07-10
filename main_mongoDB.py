# mongoDB python client
import pymongo
import datetime

# connecting to mongoDB
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


def add_tool(project_id,sender=None):
    tool_id = int(input("tool id:-> "))
    quantity = int(input("Quantity:-> "))
    if sender:
        project_info = get_project_info(sender)
        tool_info = project_info.find_one({"_id":sender})["avl"][str(tool_id)]
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
                                f"avl.{tool_id}.from.{i}":f"{day}/{month}/{year}",
                                f"avl.{tool_id}.sender.{i}":'pre_exist'
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
        
            if project_id not in main.find_one({"_id":tool_id})["pid"]:
                        main.update_one({"_id":tool_id},
                        {
                            "$push":{
                                "pid":project_id
                            }
                        })
        else:
            print('insufficient quantity')    

def create_new_project():
    #project details
    project_id = projects.count()+1
    project_name = input("enter project name:-> ")
    city = input('select city:-> ')
    projects.insert_one({
            "_id":project_id,
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


if __name__ == "__main__":
    db.close()
