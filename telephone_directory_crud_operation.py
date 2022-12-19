client = pymongo.MongoClient("mongodb+srv://<Username>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
db = client.Telecom
records=db.phonebook
mylist_1 = [
    {"Name": "Soni", "phone number": 1234567890, "place": "Mumbai"},
    {"Name": "Soniya", "phone number": 2345678901, "place": "Delhi"},
    {"Name": "Sam", "phone number": 3456789012, "place": "Goa"},
    {"Name": "John", "phone number": 4567890123, "place": "Chennai"},
    {"Name": "Sana", "phone number": 5678901234, "place": "Shimla"},
]
#Create Database
x=records.insert_many(mylist_1)

#Find/Retrieve data
for y in records.find():
  print(y)
  
#Delete dataset
records.delete_one({"Name": "Sana", "phone number": 5678901234, "place": "Shimla"})

#Update dataset
mylist_1 = {"Name": "john"}
newvalue = {"$set":{"place":"Chennai","phone number": 9874563210}}

records.update_one(mylist_1,newvalue)
