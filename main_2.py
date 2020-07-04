import pymongo

db = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = db["testdb"]
