# File: simulation/attack_bot.py

import random
import logging
import time
from faker import Faker
from psycopg2 import sql
from database.config import get_db_connection
from simulation.utils import get_logger, log_to_csv

# Initialize logger
log = get_logger("attack_bot")

# Initialize Faker
fake = Faker()

def get_db_data(cursor, table_name, column_name):
    """Fetch IDs from a given table."""
    try:
        query = sql.SQL("SELECT {} FROM {};").format(sql.Identifier(column_name), sql.Identifier(table_name))
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        log.error(f"Error retrieving data from {table_name}: {e}")
        return []

def log_attack_query(cursor, user_id, query, attack_type):
    try:
        sql_insert = "INSERT INTO db_logs (user_id, query, is_normal, attack_type) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql_insert, (user_id, query, False, attack_type))

        # Log into our CSV too
        log_to_csv(user_id, query, is_normal=False, attack_type=attack_type)

    except Exception as e:
        log.error(f"Failed to log malicious query for user {user_id}: {e}")
        raise

# --- Attack Payloads ---

def sql_injection_payload():
    """Pick a random SQL injection payload."""
    payloads = [
        "' OR 1=1 --",
        "' UNION SELECT NULL, table_name, NULL, NULL FROM information_schema.tables --",
        "' OR 1=pg_sleep(5) --",
        "'; DELETE FROM users; --",
        "'; SELECT version(); --"
    ]
    return random.choice(payloads)

def buffer_overflow_payload(base_length=200):
    """Generate a long string payload for overflow simulation."""
    long_string = "A" * (base_length + random.randint(10, 50))
    payloads = [
        f"SELECT * FROM products WHERE product_name = '{long_string}';",
        f"INSERT INTO reviews (product_id, user_id, rating, review_text) VALUES ('1', '1', 5, '{long_string}');",
        f"UPDATE users SET shipping_address = '{long_string}' WHERE user_id = '1';"
    ]
    return random.choice(payloads)

# --- Attack Functions ---

def simulate_sql_injection(cursor, user_id, product_ids):
    if not product_ids:
        return
    product_id = random.choice(product_ids)
    attack_payload = sql_injection_payload()
    query_str = f"INSERT INTO reviews (product_id, user_id, rating, review_text) VALUES ('{product_id}', '{user_id}', 5, '{attack_payload}');"

    try:
        cursor.execute(query_str)  # may fail, but that’s fine
    except Exception as e:
        log.warning(f"[SQLi] Query failed (expected): {e}")

    log_attack_query(cursor, user_id, query_str, "SQLi")
    log.warning(f"💀 User {user_id} launched SQLi on product {product_id}")

def simulate_buffer_overflow(cursor, user_id):
    query_str = buffer_overflow_payload()

    try:
        cursor.execute(query_str)  # may fail, that’s okay
    except Exception as e:
        log.warning(f"[Buffer Overflow] Query failed (expected): {e}")

    log_attack_query(cursor, user_id, query_str, "Buffer Overflow")
    log.warning(f"💀 User {user_id} launched Buffer Overflow attack")

def simulate_malicious_activity(user_id):
    """Run a session for one malicious user."""
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        product_ids = get_db_data(cursor, 'products', 'product_id')

        for _ in range(random.randint(1, 3)):  # multiple attacks
            attack_type = random.choice(["SQLi", "Buffer Overflow"])
            if attack_type == "SQLi":
                simulate_sql_injection(cursor, user_id, product_ids)
            else:
                simulate_buffer_overflow(cursor, user_id)

            conn.commit()
            time.sleep(random.uniform(0.1, 0.5))

        log.critical(f"[Malicious User {user_id}] Injected multiple payloads.")
    except Exception as e:
        log.error(f"Error in malicious activity for {user_id}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    log.info("🚨 Testing attack bot with one malicious user...")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        users = get_db_data(cursor, 'users', 'user_id')
        cursor.close()
        conn.close()
        if users:
            simulate_malicious_activity(users[0])