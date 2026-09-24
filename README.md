# Attendance Marking System (CLI)

## Overview

The Attendance Marking System is a simple Python-based command-line project.

It is used to add students, mark their daily attendance, and check attendance reports. The project uses SQLite to save the data, so the information is not lost when the program is closed.

The project works offline and does not need a GUI, internet connection, or any external service.

For the complete problem statement, see `statement.md`.

## Features

1. **Add Student** - Add a student using their roll number and name.

2. **Mark Attendance** - Mark a student as Present or Absent for a selected date. If no date is entered, today's date is used.

3. **View Attendance for a Date** - Check the attendance of all students for a particular date.

4. **View Attendance Percentage** - Check the attendance percentage of a particular student.

5. **View Overall Summary** - See the total present days, total attendance days, and percentage of each student.

6. **List All Students** - Display all the students registered in the system.

7. **Save Data** - Student and attendance data is saved automatically in `attendance.db`.

8. **Logging** - Important actions and errors are saved in `app.log`.

## Technologies Used

- **Python 3**
- **SQLite** - Used to store student and attendance data.
- **unittest** - Used for testing the program.
- **Matplotlib** - Used only for creating project diagrams. It is not required to run the main program.

The main project uses Python's standard library, so no extra packages are needed to run it.

## Project Structure

```text
attendance-system/

├── main.py                  # Main program and menu
├── database.py              # Database connection and tables
├── student_service.py       # Student related functions
├── attendance_service.py   # Attendance related functions
├── report_service.py        # Attendance reports
├── utils.py                 # Input checking functions
├── logger_config.py         # Logging setup
├── requirements.txt         # Project dependencies
├── statement.md             # Problem statement
│
├── tests/
│   └── test_attendance.py   # Unit tests
│
├── docs/
│   ├── generate_diagrams.py
│   ├── architecture_diagram.png
│   ├── use_case_diagram.png
│   ├── workflow_diagram.png
│   ├── class_diagram.png
│   ├── sequence_diagram.png
│   ├── er_diagram.png
│   └── screenshot_cli_session.png
│
└── .gitignore