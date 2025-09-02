# File: simulation/utils.py

import os
import csv
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# --- Setup paths ---
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
CSV_FILE = os.path.join(LOGS_DIR, "simulation_data.csv")

os.makedirs(LOGS_DIR, exist_ok=True)

# --- Logger setup ---
def get_logger(name: str):
    """
    Returns a configured logger instance that logs to console + file.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Avoid duplicate handlers
    
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    # Rotating file handler
    file_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, f"{name}.log"), maxBytes=5_000_000, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# --- CSV logging ---
def log_to_csv(user_id, query, is_normal, attack_type=None):
    """
    Append a row to the CSV dataset file.
    Fields: timestamp, user_id, query, is_normal, attack_type
    """
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "user_id", "query", "is_normal", "attack_type"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            user_id,
            query,
            is_normal,
            attack_type if attack_type else ""
        ])
