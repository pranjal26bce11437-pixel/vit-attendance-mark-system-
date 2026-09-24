# Tests for the attendance system

import sys
import os
import unittest

# Add project folder to the path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database import get_connection, initialize_database
from student_service import StudentService
from attendance_service import AttendanceService
from report_service import ReportService
from utils import is_valid_roll_no, is_valid_name, is_valid_date


class TestUtils(unittest.TestCase):

    def test_valid_roll_no(self):
        self.assertTrue(is_valid_roll_no("101"))
        self.assertTrue(is_valid_roll_no("VIT-2026"))
        self.assertFalse(is_valid_roll_no(""))
        self.assertFalse(is_valid_roll_no("has space"))

    def test_valid_name(self):
        self.assertTrue(is_valid_name("Rahul Sharma"))
        self.assertFalse(is_valid_name(""))
        self.assertFalse(is_valid_name("   "))
        self.assertFalse(is_valid_name("1234"))

    def test_valid_date(self):
        self.assertTrue(is_valid_date("2026-09-22"))
        self.assertFalse(is_valid_date("22-09-2026"))
        self.assertFalse(is_valid_date("not-a-date"))


class TestStudentService(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(":memory:")
        initialize_database(self.conn)
        self.students = StudentService(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_add_student(self):
        success, message = self.students.add_student(
            "101", "Rahul Sharma"
        )
        self.assertTrue(success)
        self.assertIn("added successfully", message)

    def test_duplicate_student(self):
        self.students.add_student("101", "Rahul Sharma")

        success, message = self.students.add_student(
            "101", "Someone Else"
        )

        self.assertFalse(success)
        self.assertIn("already exists", message)

    def test_empty_name(self):
        success, message = self.students.add_student("102", "")

        self.assertFalse(success)

    def test_student_exists(self):
        self.students.add_student("101", "Rahul Sharma")

        self.assertTrue(
            self.students.student_exists("101")
        )

        self.assertFalse(
            self.students.student_exists("999")
        )


class TestAttendanceService(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(":memory:")
        initialize_database(self.conn)

        self.students = StudentService(self.conn)
        self.attendance = AttendanceService(self.conn)

        self.students.add_student("101", "Rahul Sharma")

    def tearDown(self):
        self.conn.close()

    def test_mark_attendance(self):
        success, message = self.attendance.mark_attendance(
            "101", "2026-09-22", "Present"
        )

        self.assertTrue(success)

    def test_invalid_date(self):
        success, message = self.attendance.mark_attendance(
            "101", "not-a-date", "Present"
        )

        self.assertFalse(success)

    def test_update_attendance(self):
        self.attendance.mark_attendance(
            "101", "2026-09-22", "Present"
        )

        success, message = self.attendance.mark_attendance(
            "101", "2026-09-22", "Absent"
        )

        self.assertTrue(success)
        self.assertIn("updated", message.lower())

        records = self.attendance.get_student_attendance("101")

        # There should still be only one record
        self.assertEqual(len(records), 1)

        # The record should now be Absent
        self.assertEqual(records[0][1], "Absent")


class TestReportService(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection(":memory:")
        initialize_database(self.conn)

        self.students = StudentService(self.conn)
        self.attendance = AttendanceService(self.conn)
        self.reports = ReportService(self.conn)

        self.students.add_student("101", "Rahul Sharma")

        self.attendance.mark_attendance(
            "101", "2026-09-20", "Present"
        )

        self.attendance.mark_attendance(
            "101", "2026-09-21", "Present"
        )

        self.attendance.mark_attendance(
            "101", "2026-09-22", "Absent"
        )

    def tearDown(self):
        self.conn.close()

    def test_attendance_percentage(self):
        percentage, total = self.reports.attendance_percentage("101")

        self.assertEqual(total, 3)
        self.assertAlmostEqual(percentage, 66.67, places=1)

    def test_no_attendance(self):
        self.students.add_student("102", "Priya Verma")

        percentage, total = self.reports.attendance_percentage("102")

        self.assertEqual(percentage, 0.0)
        self.assertEqual(total, 0)

    def test_overall_summary(self):
        summary = self.reports.overall_summary()

        self.assertEqual(len(summary), 1)

        roll_no, name, present, total, percentage = summary[0]

        self.assertEqual(present, 2)
        self.assertEqual(total, 3)


if __name__ == "__main__":
    unittest.main()

