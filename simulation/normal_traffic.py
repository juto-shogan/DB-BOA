# File: simulation/normal_traffic.py

import random
import logging
from datetime import datetime
from database.config import get_db_connection

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

def log_query(cursor, user_id, query):
    """Insert executed query into db_logs for ML later."""
    cursor.execute(
        "INSERT INTO db_logs (user_id, query, timestamp) VALUES (%s, %s, %s)",
        (user_id, query, datetime.utcnow())
    )

def simulate_browse_products(cursor, user_id):
    """Simulate a user browsing products."""
    query = "SELECT product_id, product_name, price FROM products ORDER BY RANDOM() LIMIT 5;"
    cursor.execute(query)
    products = cursor.fetchall()
    log.info(f"[User {user_id}] Browsed products: {products}")
    log_query(cursor, user_id, query)

def simulate_place_order(cursor, user_id):
    """Simulate a user placing an order with one product."""
    cursor.execute("SELECT product_id, price FROM products ORDER BY RANDOM() LIMIT 1;")
    product = cursor.fetchone()
    if not product:
        return
    product_id, price = product
    quantity = random.randint(1, 3)
    total_amount = price * quantity

    # Insert into orders
    cursor.execute(
        "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s) RETURNING order_id;",
        (user_id, total_amount, "pending")
    )
    order_id = cursor.fetchone()[0]

    # Insert into order_items
    cursor.execute(
        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s);",
        (order_id, product_id, quantity, price)
    )

    log.info(f"[User {user_id}] Placed order {order_id} for {quantity}x product {product_id}")
    log_query(cursor, user_id, f"INSERT INTO orders (...) VALUES ({user_id}, {total_amount}, 'pending');")

def simulate_write_review(cursor, user_id):
    """Simulate a user writing a product review."""
    cursor.execute("SELECT product_id FROM products ORDER BY RANDOM() LIMIT 1;")
    product = cursor.fetchone()
    if not product:
        return
    product_id = product[0]
    rating = random.randint(1, 5)
    review_text = random.choice([
        "Great product, highly recommend!",
        "It’s okay, could be better.",
        "Not worth the money.",
        "Amazing quality!",
        "Works as expected."
    ])

    cursor.execute(
        "INSERT INTO reviews (product_id, user_id, rating, review_text) VALUES (%s, %s, %s, %s);",
        (product_id, user_id, rating, review_text)
    )
    log.info(f"[User {user_id}] Wrote review on product {product_id}")
    log_query(cursor, user_id, f"INSERT INTO reviews (...) VALUES ({product_id}, {user_id}, {rating}, ...);")

def simulate_user_activity(user_id):
    """Run a simulated session for one user (2–4 random actions)."""
    conn = get_db_connection()
    if not conn:
        log.error("Database connection failed. Exiting simulation.")
        return
    cursor = conn.cursor()

    try:
        actions = [simulate_browse_products, simulate_place_order, simulate_write_review]
        for _ in range(random.randint(2, 4)):  # Each session has 2–4 actions
            action = random.choice(actions)
            action(cursor, user_id)

        conn.commit()
        log.info(f"[User {user_id}] Session completed successfully.")
    except Exception as e:
        log.error(f"Error during user simulation: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Example: simulate 3 random users once
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users ORDER BY RANDOM() LIMIT 3;")
    users = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    for uid in users:
        simulate_user_activity(uid)
