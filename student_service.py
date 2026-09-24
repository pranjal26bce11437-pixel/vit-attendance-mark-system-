# Student add karne aur check karne ke functions

import sqlite3
import logging
from utils import is_valid_roll_no, is_valid_name

logger = logging.getLogger("attendance_system")


class StudentService:
    def __init__(self, conn):
        self.db = conn

    def add_student(self, roll_no, name):
        # Naya student add karta hai
        roll_no = roll_no.strip()
        name = name.strip()

        if not is_valid_roll_no(roll_no):
            return False, "Invalid roll number. Use only letters, numbers, '-', '_' or '/' (max 20 chars)."

        if not is_valid_name(name):
            return False, "Invalid name. Name cannot be empty and must contain letters."

        try:
            self.db.execute(
                "INSERT INTO students (roll_no, name) VALUES (?, ?)",
                (roll_no, name)
            )
            self.db.commit()

            # Log mein daal diya, taaki pata rahe kaun add hua
            logger.info(f"Added student {roll_no} ({name}).")

            return True, f"Student '{name}' ({roll_no}) added successfully."

        except sqlite3.IntegrityError:
            logger.warning(f"Attempted to add duplicate roll number {roll_no}.")
            return False, f"A student with roll number '{roll_no}' already exists."

    def student_exists(self, roll_no):
        cursor = self.db.execute(
            "SELECT 1 FROM students WHERE roll_no = ?", (roll_no,)
        )
        return cursor.fetchone() is not None

    def list_students(self):
        cursor = self.db.execute(
            "SELECT roll_no, name FROM students ORDER BY roll_no"
        )
        return cursor.fetchall()

    def get_student(self, roll_no):
        cursor = self.db.execute(
            "SELECT roll_no, name FROM students WHERE roll_no = ?", (roll_no,)
        )
        return cursor.fetchone()