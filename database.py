from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Підключення до бази (PostgreSQL через DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 📋 Модель таблиці користувачів
class User(Base):
    tablename = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)

# 📋 Модель таблиці запитів
class Request(Base):
    tablename = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    command = Column(String)
    text = Column(String)

# 📋 Модель таблиці аудитів
class Audit(Base):
    tablename = "audits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    niche = Column(String)
    city = Column(String)
    average_check = Column(String)
    ads = Column(String)

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

# 📋 Додавання аудиту
def add_audit(user_id, niche, city, average_check, ads):
    session = SessionLocal()
    new_audit = Audit(
        user_id=user_id,
        niche=niche,
        city=city,
        average_check=average_check,
        ads=ads
    )
    session.add(new_audit)
    session.commit()
    session.close()

# 📋 Отримати всіх користувачів
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return [(user.id, user.username) for user in users]
