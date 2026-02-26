import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE,
            username TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_user(telegram_id, username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, username)
        VALUES (%s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
    """, (telegram_id, username))
    conn.commit()
    cur.close()
    conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT telegram_id FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users
