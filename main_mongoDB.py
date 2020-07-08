# mongoDB python client
import pymongo
import time

# connecting to mongoDB
db = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = db["testdb"]
main = mydb["main"]
projects = mydb["projects"]
tool_history = mydb["tool_history"]


def get_tools():
    # return list(main.find())
    print("id   name   quant") 
    for i in main.find(): 
        print(str(i["_id"])+"   "+i["tool"]+"      "+str(i["quant"])) 

def get_tool_info(tool_id):
    return main.find_one({"_id":tool_id})


def add_tool(project_id,sender=None):
    tool_id = int(input('enter tool id:-> '))
    quantity = int(input('enter quantity:-> '))
    if sender:
        project_info = get_project_info(sender)
        project_name = project_info['proj_name']
        avl_quant = int(project_info["tools"][str(tool_id)][1])
        sr_num = project_info["tools"][str(tool_id)][0]
        sr_num = sr_num.split("_")
        sr_num = sr_num[0]+'_'+str((avl_quant-quantity)+1)
        if quantity<=avl_quant:
            if quantity==avl_quant:
                projects.update_one({"_id":sender},{"$unset":{"tools."+str(tool_id):project_info["tools"][str(tool_id)]}})
            else:
                projects.update_one({"_id":sender},{"$set":{"tools."+str(tool_id)+".1":avl_quant-quantity}})
            projects.update_one({"_id":project_id},{"$set":{"tools."+str(tool_id):[sr_num,quantity,project_name]}})
            main.update_one({"_id":tool_id},{"$set":{"history."+str(project_id):[sr_num,quantity]}})
            return "tool added"
        else:
            return "insufficient quantity"
    else:
        tool_info = get_tool_info(tool_id)
        avl_quant = int(tool_info["quant"])
        sr_num = tool_info["sr_num"]
        sr_num = sr_num.split("_")
        sr_num = sr_num[0]+'_'+str((avl_quant-quantity)+1)
        if quantity<=avl_quant:
            projects.update_one({"_id":project_id},{"$set":{"tools."+str(tool_id):[sr_num,quantity,"main"]}})
            main.update_one({"_id":tool_id},{"$set":{"quant":avl_quant-quantity,"history."+str(project_id):[sr_num,quantity]}})
            return f"tool {tool_id}. {tool_info['tool']} added"
        else:
            return f"insufficient quantity for tool:-> ({tool_id}. {tool_info['tool']})"


def create_new_project():
    #project details
    project_id = projects.count()+1
    project_name = input("enter project name:-> ")
    city = input('select city:-> ')
    print("select tools ->\n\n")
    projects.insert_one({"_id":project_id,'proj_name':project_name,'city':city,"tools":{},"status":"active"})
    time.sleep(2)
    get_tools()
    #adding tools
    while True:
        i=add_tool(project_id)
        if i:
            print(i)
    
    print(get_project_info(project_id))

def get_projects():
    for i in projects.find():
        print(i)

def get_project_info(project_id):
    return projects.find_one({"_id":project_id})

def delete_project(project_id):
    pass


if __name__ == "__main__":
    add_tool(2,1)
    db.close()