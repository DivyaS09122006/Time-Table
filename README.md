---
# Time-Table

**College Timetable Scheduler** — A Python project to generate and manage class timetables for courses, faculty, and student groups. Includes both an admin scheduler and a student timetable viewer. 📅

This project automates the creation and visualization of college timetables. It handles course scheduling, faculty availability, and student group constraints to produce conflict-free timetables. Students can also view their personalized schedule using the student viewer module.

---

## ✨ Features

### 🏫 Admin Scheduler

* Generates a timetable based on days, slots, rooms, faculties, and courses.
* Ensures no faculty or room is double-booked.
* Supports flexible slot durations (e.g., 30 mins, 1 hr, 1.5 hrs).
* Stores data in constraint matrices for easy manipulation and visualization.

### 👩‍🎓 Student Viewer

* Students can query their batch timetable easily.
* Provides clean tabular output using pandas.
* Can visualize daily and weekly schedules.

### 🎨 Unique Approach

* Scheduling is conceptualized like a **checkerboard layering problem**:
  Each `day × time slot × room` is a cell.
  Faculty, course, and student availability act as colored overlays.
* Conflicts are detected when overlays collide, ensuring conflict-free timetables.
* This analogy helped design intuitive constraint matrices for the scheduler.

---

## 🛠️ Tech Stack

* **Python 3.12+**
* **NumPy** → matrix-based timetable representation
* **Pandas** → student timetable viewer
* **Matplotlib** → optional, for visualizations

---

## 📂 Project Structure

```
Time-Table/
│
├── Time_table.py        # Core scheduler logic (admin view)
├── Student_viewer.py    # Student timetable viewer
├── README.md            # Project documentation
└── .gitignore           # Ignore unnecessary files
```

---

## 🚀 Getting Started

1️⃣ **Clone the repository**

```bash
git clone https://github.com/DivyaS09122006/Time-Table.git
cd Time-Table
```

2️⃣ **Install dependencies**

```bash
pip install numpy pandas
```

3️⃣ **Run the scheduler**

```bash
python Time_table.py
```

4️⃣ **Run the student viewer**

```bash
python Student_viewer.py
```

---

## 🧪 Example Output

**Batch A Timetable Sample**

| Day       | 09:00-10:00           | 10:30-11:30             | 14:00-15:00            |
| --------- | --------------------- | ----------------------- | ---------------------- |
| Monday    | Ethics & Environment  | Design Analysis         | —                      |
| Tuesday   | Software Design Tools | Computer Networks       | Differential Equations |
| Wednesday | Design Analysis       | Computer Networks (Tut) | Elective               |

> (Sample data based on provided timetable image)

---
