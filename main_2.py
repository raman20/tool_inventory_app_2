# mongoDB python client
import pymongo

# connecting to mongoDB
db = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = db["testdb"]
main = mydb["main"]
projects = mydb["projects"]


def get_tools():
    # return list(main.find())
    print("id   name   quant") 
    for i in main.find(): 
        print(str(i["_id"])+"   "+i["tool"]+"      "+str(i["quant"])) 

def get_tool_info(id):
    return main.find_one({"__id":id})


def create_new_project():

    project_id = projects.count()+1
    project_name = input("enter project name:-> ")
    city = input('select city:-> ')
    print("select tools ->\n\n")
    get_tools()
    tool_id = int(input('enter tool id:-> '))
    quantity = int(input('enter quantity:-> '))
    tool_info = get_tool_info(tool_id)
    avl_quant = tool_info["quant"]
    sr_num = tool_info["sr_num"]
    sr_num = sr_num.split("_")
    sr_num = sr_num[0]+'_'+str((avl_quant-quantity)+1)
    if quantity<=avl_quant:
        projects.insert_one({"_id":project_id,'proj_name':project_name,'city':city,"tools":{"tool_id":[sr_num,quantity]}})
        main.update_one({"_id":str(tool_id)},{"$set":{"quant":(avl_quant-quantity),"loc."+city:[sr_num,quantity]}})
    else:
        print("insufficient quantity")
        return

    get_project_info(project_id)

def get_projects():
    pass

def get_project_info(id):
    print(projects.find_one({"_id":id}))

def add_tool():
    pass