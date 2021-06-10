import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Students"]

mycol = mydb["StudentDetails"]

def Attendance(roll):
    x = mycol.find_one({"roll":roll})
    if not x["present"]:
        mycol.update({"roll": roll}, {"$set" : {"present": True}})
        print(f"Attendance marked for {roll} successfully!!")
