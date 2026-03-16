from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    tablename = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)

def create_table():
    Base.metadata.create_all(bind=engine)

def add_user(user_id, username):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        new_user = User(id=user_id, username=username)
        session.add(new_user)
        session.commit()
    session.close()

def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return [(u.id, u.username) for u in users]
