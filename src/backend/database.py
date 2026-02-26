from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    1回のリクエストごとにデータベースセッションを作成し、
    処理が終わったら確実にセッションを閉じるためのジェネレータ関数
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
