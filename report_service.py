# Attendance ka report/summary banane ke functions

import logging

logger = logging.getLogger("attendance_system")

class ReportService:
    def __init__(self, conn):
        self.db = conn

    def attendance_for_date(self, on_date):
        # Date ka attendance report
        cursor = self.db.execute("""
            SELECT s.roll_no, s.name, COALESCE(a.status, 'Not Marked')
            FROM students s
            LEFT JOIN attendance a
            ON s.roll_no = a.roll_no AND a.date = ?
            ORDER BY s.roll_no
        """, (on_date,))
        return cursor.fetchall()

    def attendance_percentage(self, roll_no):
        # Student attendance percentage
        cursor = self.db.execute("""
            SELECT status, COUNT(*) FROM attendance
            WHERE roll_no = ?
            GROUP BY status
        """, (roll_no,))

        counts = dict(cursor.fetchall())
        present = counts.get("Present", 0)
        absent = counts.get("Absent", 0)
        total = present + absent

        if total == 0:
            return 0.0, 0

        percentage = round((present / total) * 100, 2)
        return percentage, total

    def overall_summary(self):
        # Overall class summary
        cursor = self.db.execute("""
            SELECT s.roll_no, s.name,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
                   COUNT(a.id) AS total_days
            FROM students s
            LEFT JOIN attendance a ON s.roll_no = a.roll_no
            GROUP BY s.roll_no
            ORDER BY s.roll_no
        """)

        rows = cursor.fetchall()
        summary = []

        for roll_no, name, present_days, total_days in rows:
            present_days = present_days or 0
            total_days = total_days or 0

            pct = round(
                (present_days / total_days) * 100, 2
            ) if total_days else 0.0

            summary.append(
                (roll_no, name, present_days, total_days, pct)
            )

        return summary