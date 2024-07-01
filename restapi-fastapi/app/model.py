from __future__ import annotations
from os import environ
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient

# データベース接続情報を環境変数から取得
CONNECTION_STRING = (
    f"mongodb://"
    f"{environ.get('DB_USER')}:"
    f"{environ.get('DB_PASSWORD')}@"
    f"{environ.get('DB_HOST')}:"
    f"{environ.get('DB_PORT')}/?authSource=admin"
)

# データベース接続・コレクション取得
client: AgnosticClient = AsyncIOMotorClient(CONNECTION_STRING)
database: AgnosticDatabase = client[environ.get('DB_NAME')] # データベース名
collection: AgnosticCollection = database["db_calender"] # コレクション名

# Calender エンティティを表すクラス
class Calender(BaseModel):
    id: Optional[str] = None
    content: Optional[str]
    event_id:Optional[int] = None
    created_date: Optional[datetime] = None
    alterted_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    # MongoDB ドキュメントID を id に変換した Calender インスタンスを生成します。
    @classmethod
    def from_mongo(cls, data: dict) -> Calender:
        data["id"] = str(data.pop("_id"))
        return cls(**data)

    # Calender インスタンスの id を MongoDB ドキュメントIDに変換します。
    def to_mongo(self) -> dict[str, str]:
        data = self.model_dump()
        data["_id"] = ObjectId(data.pop("id"))
        return data

    # 新しい Calender インスタンスの作成に必要なフィールドを設定します。
    def set_create_fields(self, create_dict: dict) -> None:
        create_dict["_id"] = ObjectId()
        create_dict["created_date"] = datetime.utcnow()

    # 更新されるフィールドを差分として設定します。
    def map_update_fields(self, update_dict: dict, exist_dict: dict) -> None:
        update_dict.pop("id")
        update_dict["_id"] = exist_dict["_id"]
        update_dict["created_date"] = exist_dict["created_date"]

