from fastapi import FastAPI, Query
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# Connect to MongoDB
MONGO_URI = "mongodb+srv://faishion:faishion@us-west-aws.t1dyqdx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["deals"]                    # your database
collection = db["dealmoon_by_item"]    # your collection

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}

@app.get("/products")
def search_products(q: str = Query("")):
    # Search in title, href, or product_url
    cursor = collection.find({
        "$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"href": {"$regex": q, "$options": "i"}},
            {"product_url": {"$regex": q, "$options": "i"}}
        ]
    }).limit(10)

    results = []
    for doc in cursor:
        results.append({
            "id": str(doc["_id"]),
            "title": doc.get("title"),
            "href": doc.get("href"),
            "product_url": doc.get("product_url"),
            "current_price": doc.get("current_price"),
            "original_price": doc.get("original_price"),
        })

    return {
        "count": len(results),
        "query": q,
        "results": results
    }
