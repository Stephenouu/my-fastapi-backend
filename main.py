from fastapi import FastAPI, Query
from fastapi import FastAPI, Header, HTTPException, Request
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

API_KEY = "faishion-n32tb2gnsgkasgi332gn2gskgnvzl"  # set your secret key here

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return await call_next(request)

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
