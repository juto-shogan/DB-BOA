import os
import sys
import logging
from config import get_db_connection

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# Define paths
BASE_DIR = os.path.dirname(__file__)
SCHEMA_FILE = os.path.join(BASE_DIR, 'schema.sql')
SEED_DATA_FILE = os.path.join(BASE_DIR, 'seed_data.sql')

def execute_sql_file(cursor, filepath):
    """Read and execute an SQL file with multiple statements."""
    with open(filepath, "r", encoding="utf-8") as f:
        sql_content = f.read()
        statements = sql_content.strip().split(";")
        for statement in statements:
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt + ";")

def initialize_database():
    """Initializes the database schema and seeds data."""
    log.info(" Starting database initialization...")
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            log.error("Failed to get database connection. Check your .env file.")
            sys.exit(1)

        cur = conn.cursor()

        # Run schema
        log.info(" Executing schema.sql...")
        execute_sql_file(cur, SCHEMA_FILE)

        # Run seed data
        log.info(" Executing seed_data.sql...")
        execute_sql_file(cur, SEED_DATA_FILE)

        conn.commit()
        log.info(" Database initialized successfully!")

    except Exception as e:
        log.error(f" Error during database setup: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            log.info(" Database connection closed.")

if __name__ == '__main__':
    initialize_database()