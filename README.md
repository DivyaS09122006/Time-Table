# Time-Table
College Timetable Scheduler — A Python project that generates and manages class timetables for courses, faculty, and student groups. Includes both admin scheduling logic and student timetable viewer.
📅 College Timetable Scheduler

A Python project that automates the generation and visualization of college timetables.
It handles course scheduling, faculty availability, and student group constraints to create a conflict-free timetable.
Additionally, it provides a student viewer module, so students can directly check their personalized schedule.

✨ Features

🏫 Admin Scheduler

Generates a timetable based on days, slots, rooms, faculty, and courses.

Ensures no faculty or room is double-booked.

Supports flexible slot durations (e.g., 30 mins, 1 hr, 1.5 hrs).

Stores data in constraint matrices for easy manipulation.

👩‍🎓 Student Viewer

Students can query their batch timetable.

Easy visualization of daily and weekly schedule.

Uses pandas for clean tabular output.

🎨 Unique Approach

We conceptualized scheduling like a checkerboard layering problem:

Each day × time slot × room is a cell.

Faculty, course, and student availability act as colored overlays.

Overlaps are detected when shades conflict → ensures conflict-free timetabling.

This analogy helped us design the constraint matrices intuitively.

🛠️ Tech Stack

Python 3.12+

NumPy → matrix-based timetable representation

Pandas → student timetable viewing

Matplotlib (optional, for future visualization)

📂 Project Structure
Tsubaki/
│
├── Time_table.py        # Core scheduler logic (admin view)
├── Student_viewer.py    # Student timetable viewer
├── README.md            # Project documentation
└── .gitignore           # Ignore unnecessary files

🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/DivyaS09122006/Time-Table.git
cd Time-Table

2️⃣ Install Dependencies
pip install numpy pandas

3️⃣ Run Scheduler
python Time_table.py

4️⃣ Run Student Viewer
python Student_viewer.py

🧪 Example

For Batch A, the timetable output may look like:

Day	09:00-10:00	10:30-11:30	14:00-15:00
Monday	Ethics & Environment	—	Design Analysis
Tuesday	Software Design	Computer Networks	Differential Eqns
Wednesday	Design Analysis	Computer Networks (Tut)	Elective

(Sample data based on your provided timetable image)
