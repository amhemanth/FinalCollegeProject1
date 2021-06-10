import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Students"]

mycol = mydb["StudentDetails"]

for x in mycol.find():
    x["present"] = False
    print(x)