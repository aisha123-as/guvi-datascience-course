import json
import pandas as pd
import pymongo
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
db = client.student_database
records=db.details
student_json=pd.read_json("students.json",lines=True)
d1=pd.DataFrame(student_json)
d2=d1.to_dict(orient="records")
records.insert_many(d2)


#maximum scores in all (exam, quiz and homework)
for x in records.aggregate([{"$group":{'_id': '_id', "Name" : {"$first" : "$name"},'max_marks':{'$max':'$scores'}}}]):
  print(x)
  
  
  #below average
  for i in records.aggregate([{'$project':{'_id': '$_id','below_average':{'$lt':['$score',40.00]}}}]):
  print(i)
