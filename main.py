# Main file for the attendance system

from datetime import date

from database import get_connection, initialize_database
from student_service import StudentService
from attendance_service import AttendanceService
from report_service import ReportService
from logger_config import setup_logging


def print_menu():
    print("\n===== ATTENDANCE MARKING SYSTEM =====")
    print("1. Add Student")
    print("2. Mark Attendance")
    print("3. View Attendance for a Date")
    print("4. View Attendance % for a Student")
    print("5. View Overall Summary")
    print("6. List All Students")
    print("7. Exit")


def add_student(students, attendance, reports):
    roll_no = input("Enter roll number: ")
    name = input("Enter student name: ")

    success, message = students.add_student(roll_no, name)
    print(message)


def mark_attendance(students, attendance, reports):
    roll_no = input("Enter roll number: ").strip()

    choice = input("Enter P for Present or A for Absent: ").strip().upper()

    if choice == "P":
        status = "Present"
    elif choice == "A":
        status = "Absent"
    else:
        print("Please enter P or A.")
        return

    date_input = input(
        "Enter date (YYYY-MM-DD) or press Enter for today: "
    ).strip()

    on_date = date_input if date_input else date.today().isoformat()

    success, message = attendance.mark_attendance(
        roll_no, on_date, status
    )

    print(message)


def view_attendance_for_date(students, attendance, reports):
    date_input = input(
        "Enter date (YYYY-MM-DD) or press Enter for today: "
    ).strip()

    on_date = date_input if date_input else date.today().isoformat()

    records = reports.attendance_for_date(on_date)

    if not records:
        print("No students found. Add students first.")
        return

    print("\nAttendance for", on_date)
    print("-" * 45)

    for roll_no, name, status in records:
        print(roll_no, name, status)


def view_percentage(students, attendance, reports):
    roll_no = input("Enter roll number: ").strip()

    if not students.student_exists(roll_no):
        print("Student not found.")
        return

    percentage, total_days = reports.attendance_percentage(roll_no)

    print(
        "Attendance:",
        percentage,
        "% over",
        total_days,
        "day(s)"
    )


def view_overall_summary(students, attendance, reports):
    summary = reports.overall_summary()

    if not summary:
        print("No students found.")
        return

    print("\nOverall Attendance")
    print("-" * 60)

    for roll_no, name, present, total, percentage in summary:
        print(
            roll_no,
            name,
            "Present:",
            present,
            "Total:",
            total,
            "Percentage:",
            percentage
        )


def list_students(students, attendance, reports):
    all_students = students.list_students()

    if not all_students:
        print("No students added yet.")
        return

    print("\nStudents")
    print("-" * 30)

    for roll_no, name in all_students:
        print(roll_no, name)


def main():
    logger = setup_logging()
    logger.info("Application started")

    conn = get_connection()
    initialize_database(conn)

    students = StudentService(conn)
    attendance = AttendanceService(conn)
    reports = ReportService(conn)

    while True:
        print_menu()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_student(students, attendance, reports)

            elif choice == "2":
                mark_attendance(students, attendance, reports)

            elif choice == "3":
                view_attendance_for_date(
                    students, attendance, reports
                )

            elif choice == "4":
                view_percentage(
                    students, attendance, reports
                )

            elif choice == "5":
                view_overall_summary(
                    students, attendance, reports
                )

            elif choice == "6":
                list_students(students, attendance, reports)

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            logger.error(str(e))
            print("Something went wrong:", e)

    conn.close()


if __name__ == "__main__":
    main()