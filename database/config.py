# File: database/config.py

import os
from dotenv import load_dotenv
from psycopg2 import connect as psycopg2_connect

# Load environment variables from a .env file
load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    
    This function reads database credentials from environment variables,
    which are loaded from a .env file, ensuring security.
    """
    try:
        conn = psycopg2_connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

if __name__ == '__main__':
    # This block allows you to test the connection independently
    conn = get_db_connection()
    if conn:
        print("Successfully connected to the PostgreSQL database!")
        conn.close()
    else:
        print("Failed to connect to the database.")