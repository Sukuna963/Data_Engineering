from pymongo import MongoClient


#mongodb configuration
client = MongoClient("mongodb://dio:dio@localhost:27017/")
db = client.dio
trends_collection = db.trends