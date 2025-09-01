# File: database/setup.py

import os
import sys
from psycopg2 import sql
from config import get_db_connection

# Define the paths to your SQL schema and data scripts
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), 'schema.sql')
SEED_DATA_FILE = os.path.join(os.path.dirname(__file__), 'seed_data.sql')

def initialize_database():
    """
    Initializes the PostgreSQL database by creating tables and seeding initial data.
    """
    print("--- Starting database initialization ---")
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to get database connection. Please check your .env file.")
            sys.exit(1)

        cur = conn.cursor()

        # 1. Execute schema.sql to create tables
        print("Executing schema.sql to create database tables...")
        with open(SCHEMA_FILE, 'r') as f:
            cur.execute(f.read())
        
        # 2. Execute seed_data.sql to populate tables
        print("Executing seed_data.sql to seed initial data...")
        with open(SEED_DATA_FILE, 'r') as f:
            cur.execute(f.read())

        conn.commit()
        print("Database initialization successful! 🎉")

    except Exception as e:
        print(f"An error occurred during database setup: {e}")
        if conn:
            conn.rollback() # Rollback in case of any error to maintain data integrity
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    initialize_database()