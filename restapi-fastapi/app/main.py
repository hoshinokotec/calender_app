from typing import List
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.model import collection, Calender

# app オブジェクト
app = FastAPI()

# CORS 設定：適切に修正してください。
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

# すべての Calender アイテムを取得します。
@app.get("/db_calender")
async def get_all_db_calender() -> List[Calender]:
    db_calender = []
    cursor = collection.find({})
    async for document in cursor:
        db_calender.append(Calender.from_mongo(document))
    return db_calender

# 完了した Calender アイテムを取得します。
@app.get("/db_calender/complete")
async def get_completed_db_calender() -> List[Calender]:
    db_calender = []
    cursor = collection.find({"completed_date": {"$ne": None}})
    async for document in cursor:
        db_calender.append(Calender.from_mongo(document))
    return db_calender

# ID で Calender アイテムを取得します。
@app.get("/db_calender/{id}")
async def get_Calender(id: str) -> Calender:
    document = await collection.find_one({"_id": ObjectId(id)})
    Calender = Calender.from_mongo(document)
    return Calender

# 新しい Calender アイテムを追加します。
@app.post("/db_calender")
async def create_Calender(create: Calender) -> Calender:
    create_dict = create.model_dump()
    create.set_create_fields(create_dict)
    new_Calender = Calender.from_mongo(create_dict)
    await collection.insert_one(new_Calender.to_mongo())
    return new_Calender

# 既存の Calender アイテムを更新します。
@app.put("/db_calender/{id}")
async def update_Calender(id: str, update: Calender) -> None:
    exist_dict = await collection.find_one({"_id": ObjectId(id)})
    update_dict = update.model_dump()
    update.map_update_fields(update_dict, exist_dict)
    await collection.update_one({"_id": ObjectId(id)}, {"$set": update_dict})
    return None

# ID で Calender アイテムを削除します。
@app.delete("/db_calender/{id}")
async def delete_Calender(id: str) -> None:
    await collection.delete_one({"_id": ObjectId(id)})
    return None

