import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Students"]

mycol = mydb["StudentDetails"]

stdDetails =[{"name": "AM Hemanth", "roll": "17121A1504", "mobile": "7330958302", 
                "email": "amhemanth1999@gmail.com"},
            {"name": "B Kousthubha", "roll": "17121A1514", "mobile": "123456789", 
                "email": "bollavaramkousthubha65@gmail.com"},
            {"name": "C Brundha", "roll": "17121A1518", "mobile": "123456789", 
                "email": "brundarika5993@gmail.com"},
            {"name": "C Netra", "roll": "17121A1515", "mobile": "123456789", 
                "email": "netra.chakalijune30@gmail.com"},
            {"name": "K Lohitha", "roll": "17121A1544", "mobile": "123456789", 
                "email": "kakarlalohitha@gmail.com"},
            ]
mycol.insert_many(stdDetails)
print("Inserted student details!!")
# for x in mycol.find():
#     print(x)
