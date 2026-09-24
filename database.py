# Database connect aur tables banane ke functions

import sqlite3
import logging

DATABASE_FILE = "attendance.db"

logger = logging.getLogger("attendance_system")


def get_connection(db_name=DATABASE_FILE):
    # Database connection
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database(conn):
    # Tables create karta hai
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
            FOREIGN KEY (roll_no) REFERENCES students(roll_no),
            UNIQUE(roll_no, date)
        )
    """)

    conn.commit()

    # Ho gaya, tables ban gaye
    logger.info("Database initialized (tables verified/created).")