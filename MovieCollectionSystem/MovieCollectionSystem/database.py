"""
database.py
-----------
Keeps the MySQL connection code in ONE place.
Every route in app.py calls get_connection() to talk to the database.
"""

import mysql.connector

# ---- Change these values to match YOUR MySQL setup ----
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "kajal",   # <-- put your MySQL password here
    "database": "movie_collection",
}


def get_connection():
    """Open and return a new connection to the movie_collection database."""
    return mysql.connector.connect(**DB_CONFIG)
