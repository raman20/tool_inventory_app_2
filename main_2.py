# mongoDB python client
import pymongo

# connecting to mongoDB
db = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = db["testdb"]
main = mydb["main"]
projects = mydb["projects"]

def get_tools():
    for i in main.find():
        print(i)

def get_tool_info(id):
    return main.find_one({"__id":str(id)})


def create_new_project():
    city = input('select city:-> ')
    tool_id = int(input('enter tool id:-> '))
    quantity = int(input('enter quantity:-> '))
    tool_info = main.find_one({"_id":str(tool_id)})
    avl_quant = int(tool_info["quant"])
    tool_name = tool_info["tool"]
    sr_num = tool_info["sr_num"]
    sr_num = sr_num.split("_")
    sr_num = sr_num[0]+'_'+str((avl_quant-quantity)+1)
    new_col = mydb[city]
    if quantity<=avl_quant:
        id = new_col.count()+1
        new_col.insert_one({"_id":str(id),'name':tool_name,'sr_num':sr_num,"quant":quantity})
        main.update_one({"_id":str(tool_id)},{"$set":{"quant":str(avl_quant-quantity)}})
    else:
        print("insufficient quantity")
        return

    for i in new_col.find():
        print(i)

def get_projects():
    pass

def get_project_info():
    pass

def add_tool():
    pass