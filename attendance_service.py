# Attendance mark karne ke functions

import sqlite3
import logging
from utils import is_valid_roll_no, is_valid_date

logger = logging.getLogger("attendance_system")


class AttendanceService:
    def __init__(self, conn):
        self.db = conn

    def mark_attendance(self, roll_no, attendance_date, status):
        # Attendance mark ya update karta hai
        roll_no = roll_no.strip()
        status = status.strip().capitalize()

        if not is_valid_roll_no(roll_no):
            return False, "Invalid roll number."

        if not is_valid_date(attendance_date):
            return False, "Invalid date. Use YYYY-MM-DD."

        if status not in ("Present", "Absent"):
            return False, "Status must be Present or Absent."

        try:
            self.db.execute(
                """
                INSERT INTO attendance (roll_no, date, status)
                VALUES (?, ?, ?)
                """,
                (roll_no, attendance_date, status)
            )
            self.db.commit()

            logger.info(
                f"Attendance marked: {roll_no}, {attendance_date}, {status}"
            )

            return True, "Attendance marked successfully."

        except sqlite3.IntegrityError:
            # Already record hai to update kar do
            self.db.execute(
                """
                UPDATE attendance
                SET status = ?
                WHERE roll_no = ? AND date = ?
                """,
                (status, roll_no, attendance_date)
            )
            self.db.commit()

            logger.info(
                f"Attendance updated: {roll_no}, {attendance_date}, {status}"
            )

            return True, "Attendance updated successfully."

    def get_attendance_by_date(self, attendance_date):
        cursor = self.db.execute(
            """
            SELECT roll_no, status
            FROM attendance
            WHERE date = ?
            ORDER BY roll_no
            """,
            (attendance_date,)
        )
        return cursor.fetchall()

    def get_student_attendance(self, roll_no):
        cursor = self.db.execute(
            """
            SELECT date, status
            FROM attendance
            WHERE roll_no = ?
            ORDER BY date
            """,
            (roll_no,)
        )
        return cursor.fetchall()

    def get_attendance_percentage(self, roll_no):
        cursor = self.db.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present
            FROM attendance
            WHERE roll_no = ?
            """,
            (roll_no,)
        )

        result = cursor.fetchone()

        total = result[0]
        present = result[1] or 0

        if total == 0:
            return 0.0

        return (present / total) * 100

    def get_class_summary(self):
        cursor = self.db.execute(
            """
            SELECT
                COUNT(*) AS total_records,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present,
                SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS absent
            FROM attendance
            """
        )

        result = cursor.fetchone()

        total = result[0]
        present = result[1] or 0
        absent = result[2] or 0

        return {
            "total": total,
            "present": present,
            "absent": absent
        }