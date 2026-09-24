"""
generate_diagrams.py
---------------------
Generates the design diagrams (architecture, use case, workflow,
class, sequence, ER) required by the project report, as PNG images.

This script is a DOCUMENTATION tool only - it is NOT required to run
the actual Attendance Marking System. It uses matplotlib, which is why
it is kept separate from the app's own zero-dependency requirements.txt.

Run with:  python3 generate_diagrams.py   (from inside docs/)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Ellipse

OUT_DIR = "."


def new_fig(w=10, h=7):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc="#e8f0fe", ec="#1a4d8f", fontsize=10):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                        fc=fc, ec=ec, linewidth=1.5)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, wrap=True)
    return (x, y, w, h)


def arrow(ax, p1, p2, text="", color="#333333"):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=15,
                         color=color, linewidth=1.3)
    ax.add_patch(a)
    if text:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + 0.15, text, ha="center", fontsize=8, color=color)


# ---------------------------------------------------------------
# 1. System Architecture Diagram
# ---------------------------------------------------------------
fig, ax = new_fig(10, 6)
ax.set_title("System Architecture - Attendance Marking System", fontsize=13, weight="bold")

box(ax, 3.5, 4.7, 3, 0.9, "User (Terminal / CLI)", fc="#fff3cd", ec="#8a6d3b")
box(ax, 3.5, 3.3, 3, 0.9, "main.py\n(CLI Menu Layer)")
box(ax, 0.3, 1.7, 2.8, 0.9, "student_service.py")
box(ax, 3.6, 1.7, 2.8, 0.9, "attendance_service.py")
box(ax, 6.9, 1.7, 2.8, 0.9, "report_service.py")
box(ax, 3.5, 0.3, 3, 0.9, "database.py -> SQLite\n(attendance.db)", fc="#d4edda", ec="#2e7d32")

arrow(ax, (5, 4.7), (5, 4.2))
arrow(ax, (3.6, 3.5), (1.7, 2.6))
arrow(ax, (5, 3.3), (5, 2.6))
arrow(ax, (6.4, 3.5), (8.3, 2.6))
arrow(ax, (1.7, 1.7), (4.3, 1.2))
arrow(ax, (5, 1.7), (5, 1.2))
arrow(ax, (8.3, 1.7), (5.7, 1.2))

fig.savefig(f"{OUT_DIR}/architecture_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 2. Process Flow / Workflow Diagram
# ---------------------------------------------------------------
fig, ax = new_fig(10, 7)
ax.set_title("Process Flow - Marking Attendance", fontsize=13, weight="bold")

steps = [
    (6, "Start: Launch CLI\n(python3 main.py)"),
    (5, "Display Menu"),
    (4, "User selects\n'Mark Attendance'"),
    (3, "Enter Roll No,\nStatus, Date"),
    (2, "Validate input &\ncheck student exists"),
    (1, "Save / Update record\nin SQLite"),
    (0, "Show confirmation\nmessage, return to Menu"),
]
for y, label in steps:
    box(ax, 3, y * 0.85 + 0.2, 4, 0.65, label, fontsize=9)
for i in range(len(steps) - 1):
    y1 = steps[i][0] * 0.85 + 0.2
    y2 = steps[i + 1][0] * 0.85 + 0.85
    arrow(ax, (5, y1), (5, y2))

fig.savefig(f"{OUT_DIR}/workflow_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 3. Use Case Diagram
# ---------------------------------------------------------------
fig, ax = new_fig(9, 7)
ax.set_title("Use Case Diagram - Attendance Marking System", fontsize=13, weight="bold")

# Actor (stick figure, simplified as circle + label)
ax.add_patch(Ellipse((1, 5.5), 0.5, 0.5, fc="#fff3cd", ec="#8a6d3b"))
ax.plot([1, 1], [5.25, 4.5], color="#8a6d3b")
ax.plot([0.7, 1.3], [5.0, 5.0], color="#8a6d3b")
ax.plot([1, 0.7], [4.5, 4.0], color="#8a6d3b")
ax.plot([1, 1.3], [4.5, 4.0], color="#8a6d3b")
ax.text(1, 3.6, "Administrator /\nTeacher", ha="center", fontsize=9)

use_cases = [
    (6, "Add Student"),
    (5, "Mark Attendance"),
    (4, "View Attendance\nby Date"),
    (3, "View Attendance %\nfor a Student"),
    (2, "View Overall\nSummary"),
    (1, "List All Students"),
]
for y, label in use_cases:
    ax.add_patch(Ellipse((5.5, y), 3.2, 0.8, fc="#e8f0fe", ec="#1a4d8f"))
    ax.text(5.5, y, label, ha="center", va="center", fontsize=9)
    arrow(ax, (1.4, 5.0), (3.9, y))

fig.savefig(f"{OUT_DIR}/use_case_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 4. Class / Component Diagram
# ---------------------------------------------------------------
fig, ax = new_fig(11, 7)
ax.set_title("Class Diagram - Attendance Marking System", fontsize=13, weight="bold")

box(ax, 0.3, 4.5, 3, 2, "StudentService\n- conn\n+ add_student()\n+ student_exists()\n+ list_students()\n+ get_student()",
    fontsize=8.5)
box(ax, 4, 4.5, 3, 2, "AttendanceService\n- conn\n- student_service\n+ mark_attendance()\n+ attendance_for_student()",
    fontsize=8.5)
box(ax, 7.7, 4.5, 3, 2, "ReportService\n- conn\n+ attendance_for_date()\n+ attendance_percentage()\n+ overall_summary()",
    fontsize=8.5)
box(ax, 4, 1.8, 3, 1.5, "database\n+ get_connection()\n+ initialize_database()", fontsize=8.5)
box(ax, 0.3, 1.8, 3, 1.5, "utils\n+ is_valid_roll_no()\n+ is_valid_name()\n+ is_valid_date()", fontsize=8.5)
box(ax, 7.7, 1.8, 3, 1.5, "logger_config\n+ setup_logging()", fontsize=8.5)
box(ax, 4, 0.2, 3, 1.2, "main (CLI)\nmenu + input handling", fc="#fff3cd", ec="#8a6d3b", fontsize=8.5)

arrow(ax, (5.5, 4.5), (5.5, 3.3))
arrow(ax, (1.8, 4.5), (5.5, 1.5))
arrow(ax, (5.5, 1.8), (5.5, 1.4))
arrow(ax, (9.2, 4.5), (5.5, 1.5))

fig.savefig(f"{OUT_DIR}/class_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 5. Sequence Diagram (Mark Attendance flow)
# ---------------------------------------------------------------
fig, ax = new_fig(11, 7)
ax.set_title("Sequence Diagram - Mark Attendance", fontsize=13, weight="bold")

actors = ["User", "main.py", "AttendanceService", "StudentService", "SQLite DB"]
xs = [1, 3.2, 5.6, 8, 10]
for x, name in zip(xs, actors):
    box(ax, x - 0.7, 6.2, 1.4, 0.6, name, fontsize=8)
    ax.plot([x, x], [0.3, 6.2], color="#999999", linestyle="--", linewidth=1)

messages = [
    (1, 3.2, 5.6, "1. choose 'Mark Attendance'\n+ enter roll no, status, date"),
    (3.2, 5.6, 5.0, "2. mark_attendance(roll_no, status, date)"),
    (5.6, 8, 4.4, "3. student_exists(roll_no)"),
    (8, 5.6, 3.8, "4. True/False"),
    (5.6, 10, 3.2, "5. INSERT/UPDATE attendance"),
    (10, 5.6, 2.6, "6. success"),
    (5.6, 3.2, 2.0, "7. (success, message)"),
    (3.2, 1, 1.4, "8. display confirmation"),
]
for x1, x2, y, label in messages:
    arrow(ax, (x1, y), (x2, y), label)

fig.savefig(f"{OUT_DIR}/sequence_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)


# ---------------------------------------------------------------
# 6. ER Diagram
# ---------------------------------------------------------------
fig, ax = new_fig(8, 5)
ax.set_title("ER Diagram - Attendance Marking System", fontsize=13, weight="bold")

box(ax, 0.7, 2, 3, 2.2,
    "STUDENTS\n\nroll_no (PK)\nname", fontsize=10, fc="#e8f0fe")
box(ax, 4.8, 1.3, 3, 3,
    "ATTENDANCE\n\nid (PK)\nroll_no (FK)\ndate\nstatus", fontsize=10, fc="#fff3cd")

arrow(ax, (3.7, 3.0), (4.8, 3.0), "1 : many")
ax.text(4.2, 3.25, "has", fontsize=8, style="italic")

fig.savefig(f"{OUT_DIR}/er_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("All diagrams generated successfully in the docs/ folder.")
