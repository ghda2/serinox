import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "testdb"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )
