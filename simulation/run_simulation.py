# File: simulation/run_simulation.py

import random
import logging
import threading
import time
from datetime import datetime, timedelta
from database.config import get_db_connection
from simulation.normal_traffic import simulate_user_activity

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

def get_all_users():
    """Fetch all user IDs from the database."""
    conn = get_db_connection()
    if not conn:
        log.error("Database connection failed.")
        return []
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users;")
    users = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return users

def run_concurrent_users(num_users=10, duration=None):
    """
    Simulate multiple users concurrently.
    
    Args:
        num_users (int): Number of users to simulate.
        duration (int or None): Duration in seconds to keep simulation running.
                                If None, runs each user once and exits.
    """
    all_users = get_all_users()
    if not all_users:
        log.error("No users found in the database.")
        return

    # Randomly pick users
    sampled_users = random.sample(all_users, min(num_users, len(all_users)))

    log.info(f"Starting simulation with {len(sampled_users)} users...")

    threads = []
    end_time = datetime.utcnow() + timedelta(seconds=duration) if duration else None

    def user_loop(user_id):
        """Loop actions for one user until duration expires (or just once)."""
        if duration:
            while datetime.utcnow() < end_time:
                simulate_user_activity(user_id)
                time.sleep(random.uniform(1, 3))  # small pause between actions
        else:
            simulate_user_activity(user_id)

    # Create threads
    for user_id in sampled_users:
        t = threading.Thread(target=user_loop, args=(user_id,))
        threads.append(t)
        t.start()

    # Wait for threads to finish
    for t in threads:
        t.join()

    log.info("✅ Simulation complete.")

if __name__ == "__main__":
    # Example: simulate 20 users for 60 seconds
    run_concurrent_users(num_users=20, duration=60)

    # Or, if you just want to simulate once without duration:
    # run_concurrent_users(num_users=10)