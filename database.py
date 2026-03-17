from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, index=True)    
    telegram_id = Column(Integer, unique=True, index=True)    
    username = Column(String, nullable=True)    
    
class Request(Base):
    __tablename__ = "requests"    
    id = Column(Integer, primary_key=True, index=True)    
    user_id = Column(Integer, unique=True, index=True)    
    command = Column(String)    
    text = Column(String)    
    timestamp = Column(DateTime, default=datetime.utcnow)    

def create_table():
    Base.metadata.create_all(bind=engine)    

def add_user(user_id, username):
    Session = sessionmaker(bind=engine)    
    session = Session()     
    user = session.query(User).filter(User.telegram_id == user_id).first()    
    if not user:    
        new_user = User(telegram_id=user_id, username=username)        
        session.add(new_user)        
        session.commit()
    session.close()    

def add_request(user_id, command, text):
    Session = sessionmaker(bind=engine)    
    session = Session()    
    new_request = Request(user_id=user_id, command-command, text=text)    
    session.add(new_request)    
    session.commit()        
    session.close()    

def get_all_users():
    Session = sessionmaker(bind=engine)    
    session = Session()    
    users = session.query(User).all()    
    session.close()    
    return [(u.telegram_id, u.username) for u in users]    

def get_all_requests():
    Session = sessionmaker(bind=engine)    
    session = Session()    
    request = session.query(Request).all()    
    session.close()    
    return [(r.user_id, r.command, r.text, r.timestamp) for r in requests]    
