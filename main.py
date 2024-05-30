from fastapi import Depends, FastAPI  # FastAPIフレームワークのインポート
from pydantic import BaseModel  # データ検証と設定のためのPydanticのインポート
from sqlalchemy import (Column, Integer, String,  # SQLAlchemyの主要機能のインポート
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base  # ベースクラス作成のためのインポート
from sqlalchemy.orm import Session, sessionmaker  # セッション管理のためのインポート

app = FastAPI()  # FastAPIアプリケーションのインスタンスを作成

# データベースのセットアップ
DATABASE_URL = "sqlite:///./names.db"  # SQLiteデータベースのURL
engine = create_engine(DATABASE_URL)  # データベースエンジンの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # セッションの作成
Base = declarative_base()  # ベースクラスの作成

# データベースのモデルを定義
class Name(Base):
    __tablename__ = 'names'  # テーブル名を定義
    id = Column(Integer, primary_key=True, index=True)  # idカラムを定義（プライマリキー）
    name = Column(String, index=True)  # nameカラムを定義

# テーブルの作成
Base.metadata.create_all(bind=engine)  # データベース内にテーブルを作成

# リクエストボディのモデルを定義
class NameModel(BaseModel):
    name: str  # nameフィールドを定義

# データベースセッションを取得するための依存関係を定義
def get_db():
    db = SessionLocal()  # セッションを作成
    try:
        yield db  # セッションを呼び出し元に提供
    finally:
        db.close()  # セッションを閉じる

@app.post("/submit")
async def submit_name(name: NameModel, db: Session = Depends(get_db)):
    """
    新しい名前をデータベースに挿入するエンドポイント。
    """
    new_name = Name(name=name.name)  # Nameモデルのインスタンスを作成
    db.add(new_name)  # 新しい名前をセッションに追加
    db.commit()  # トランザクションをコミットしてデータベースに保存
    db.refresh(new_name)  # 新しく追加されたデータを最新の状態にリフレッシュ
    return {"message": "Name inserted successfully"}  # 成功メッセージを返す

@app.get("/names")
async def get_names(db: Session = Depends(get_db)):
    """
    データベースから全ての名前を取得するエンドポイント。
    """
    names = db.query(Name).all()  # データベースから全ての名前をクエリ
    return [{"name": name.name} for name in names]  # 名前のリストを返す