# File: simulation/run_simulation.py

import random
import logging
import threading
import time
from datetime import datetime, timedelta
from database.config import get_db_connection
from simulation.normal_traffic import simulate_user_activity
from simulation.attack_bot import simulate_malicious_activity
from simulation.utils import get_logger

# Initialize logger
log = get_logger("orchestrator")

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

def run_simulation(num_users=10, num_attackers=2, duration=None):
    """
    Run a mixed simulation with normal + malicious users.
    
    Args:
        num_users (int): Number of normal users.
        num_attackers (int): Number of malicious users.
        duration (int or None): Duration in seconds to run. If None, runs once.
    """
    all_users = get_all_users()
    if not all_users:
        log.error("No users found in the database.")
        return

    # Pick random users for normal and malicious sessions
    random.shuffle(all_users)
    normal_users = all_users[:min(num_users, len(all_users))]
    attacker_users = all_users[min(num_users, len(all_users)):min(num_users + num_attackers, len(all_users))]

    log.info(f"Starting simulation: {len(normal_users)} normal users, {len(attacker_users)} attackers.")

    threads = []
    end_time = datetime.utcnow() + timedelta(seconds=duration) if duration else None

    def normal_user_loop(user_id):
        """Loop normal activity until duration ends (or once)."""
        if duration:
            while datetime.utcnow() < end_time:
                simulate_user_activity(user_id)
                time.sleep(random.uniform(0.5, 2))
        else:
            simulate_user_activity(user_id)

    def attacker_user_loop(user_id):
        if duration:
            while datetime.utcnow() < end_time:
                simulate_malicious_activity(user_id)
                # ⏳ stealthy attacker: 30–120 seconds between attacks
                time.sleep(random.uniform(30, 120))
        else:
            simulate_malicious_activity(user_id)

    # Launch threads for normal users
    for uid in normal_users:
        t = threading.Thread(target=normal_user_loop, args=(uid,))
        threads.append(t)
        t.start()

    # Launch threads for malicious users
    for uid in attacker_users:
        t = threading.Thread(target=attacker_user_loop, args=(uid,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    log.info("✅ Mixed simulation complete.")

if __name__ == "__main__":
    # Example: run 8 normal users + 2 attackers for 60 seconds
    run_simulation(num_users=8, num_attackers=2, duration=3600)

    # Or run a one-shot simulation without duration:
    # run_simulation(num_users=5, num_attackers=1)