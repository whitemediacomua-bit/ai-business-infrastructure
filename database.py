from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 📋 Модель таблиці користувачів
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)

# 📋 Модель таблиці запитів
class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    command = Column(String)
    text = Column(String)

# 📋 Створення таблиць
def create_table():
    Base.metadata.create_all(bind=engine)

# 📋 Додавання користувача
def add_user(user_id, username):
    session = SessionLocal()
    user = User(id=user_id, username=username)
    session.merge(user)  # merge замінює add, щоб уникнути дублювання
    session.commit()
    session.close()

# 📋 Додавання запиту
def add_request(user_id, command, text):
    session = SessionLocal()
    new_request = Request(user_id=user_id, command=command, text=text)
    session.add(new_request)
    session.commit()
    session.close()

# 📋 Отримати всіх користувачів
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return [(user.id, user.username) for user in users]

import sqlite3

def create_audit_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            niche TEXT,
            city TEXT,
            average_check TEXT,
            ads TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_audit(user_id, niche, city, average_check, ads):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audits (user_id, niche, city, average_check, ads)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, niche, city, average_check, ads))
    conn.commit()
    conn.close()
