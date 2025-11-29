import os
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=True)
    points = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://hn_user:hn_pass@db:5432/hn_db"
)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
