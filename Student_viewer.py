import pandas as pd

class StudentTimetable:
    def __init__(self):
        # Courses from your image (dummy)
        self.courses = {
            "E1": {"name": "Ethics & Environment", "room": "C205"},
            "D1": {"name": "Design Analysis of Algorithm", "room": "L11,L207,L208"},
            "B1": {"name": "Software Design Tools & Techniques", "room": "C205,L102,L106,L107"},
            "C1": {"name": "Computer Networks", "room": "C002"},
            "C2": {"name": "Differential Equations", "room": "C004"},
            "D2": {"name": "Elective", "room": ""},
        }

        # Dummy student groups (you can map IDs → courses later)
        self.students = {
            "Batch A": ["E1", "D1", "B1", "C1", "C2", "D2"],  # All courses
        }

        # Hardcoded timetable (day, start, end, code)
        self.timetable = [
            ("MON", "10:45", "12:15", "E1"),
            ("MON", "12:15", "13:15", "D1 TUT"),
            ("TUE", "09:00", "10:00", "B1"),
            ("WED", "10:00", "11:00", "C1"),
            ("WED", "11:00", "12:00", "D1"),
            ("THU", "09:00", "10:00", "D1"),
            ("THU", "10:00", "11:00", "C1"),
            ("FRI", "09:00", "10:00", "E1"),
            ("FRI", "10:00", "11:00", "B1"),
            ("TUE", "14:00", "15:30", "C2"),
            ("TUE", "15:30", "17:00", "D2"),
            ("TUE", "17:00", "17:30", "C2 TUT"),
            ("WED", "14:00", "15:30", "D1 LAB"),
            ("WED", "15:30", "17:00", "B1 LAB"),
            ("MON", "17:30", "18:30", "D2"),
        ]

    def get_student_timetable(self, student):
        """Return personal timetable for a student/batch"""
        courses = self.students[student]
        data = []
        for day, start, end, code in self.timetable:
            course_code = code.split()[0]  # handle TUT/LAB suffix
            if course_code in courses:
                cname = self.courses[course_code]["name"]
                room = self.courses[course_code]["room"]
                data.append([day, start, end, code, cname, room])
        df = pd.DataFrame(data, columns=["Day", "Start", "End", "Code", "Course", "Room"])
        return df.sort_values(["Day", "Start"])

    def export_student_timetable(self, student, filename):
        df = self.get_student_timetable(student)
        df.to_csv(filename, index=False)
        print(f"✅ Exported timetable for {student} → {filename}")


# Example usage
if __name__ == "__main__":
    sched = StudentTimetable()
    df = sched.get_student_timetable("Batch A")
    print(df)
    sched.export_student_timetable("Batch A", "BatchA_timetable.csv")
