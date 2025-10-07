import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class StudentTimetable:
    def __init__(self):
        # Comprehensive course list based on provided data
        self.courses = {
            "E1": {"name": "Ethics & Environment", "room": "C205", "faculty": "Dr. Aswath Babu H"},
            "D1": {"name": "Design Analysis of Algorithm", "room": "C205", "faculty": "Dr. Pramod Yelmewad"},
            "B1": {"name": "Software Design Tools & Techniques", "room": "C205", "faculty": "Dr. Vivekraj"},
            "C1": {"name": "Computer Networks", "room": "C002", "faculty": "Dr. Prabhu Prasad"},
            "C2": {"name": "Differential Equations", "room": "C004", "faculty": "Dr. Anand P. Barangi"},
            "D2": {"name": "Elective", "room": "Various", "faculty": "Various"},
            "CS152": {"name": "Data Science with Python", "room": "L201", "faculty": "Dr. Abdul Wahid"},
            "CS251": {"name": "2D Computer Graphics", "room": "L102", "faculty": "Dr. Vivekraj"},
            "CS261": {"name": "Operating System", "room": "C101", "faculty": "Dr. Suvadip Hazra"},
            "CS263": {"name": "Design and Analysis of Algorithms", "room": "C205", "faculty": "Dr. Pramod Yelmewad"},
            "CS264": {"name": "Computer Networks", "room": "C002", "faculty": "Dr. Prabhu Prasad"},
            "CS304": {"name": "Artificial Intelligence", "room": "C103", "faculty": "Dr. Krishnendu Ghosh"},
            "CS307": {"name": "Machine Learning", "room": "C104", "faculty": "Dr. Utkarsh Mahadeo Khaire"},
        }

        # Define multiple student batches with their courses
        self.students = {
            "Batch A": ["E1", "D1", "B1", "C1", "C2", "D2"],
            "Batch B": ["CS152", "CS261", "CS263", "CS264", "C2"],
            "Batch C": ["CS251", "CS304", "CS307", "C1", "E1"],
        }

        # Realistic timetable based on the images provided
        self.timetable = [
            # Monday
            ("MON", "09:00", "10:00", "B1", "Batch A"),
            ("MON", "10:45", "12:15", "E1", "Batch A"),
            ("MON", "12:15", "13:15", "D1 TUT", "Batch A"),
            ("MON", "14:00", "15:30", "D1 LAB", "Batch A"),
            ("MON", "17:30", "18:30", "D2", "Batch A"),
            
            # Tuesday
            ("TUE", "09:00", "10:00", "B1", "Batch A"),
            ("TUE", "10:00", "11:00", "CS152", "Batch B"),
            ("TUE", "11:00", "12:00", "E1 TUT", "Batch A"),
            ("TUE", "14:00", "15:30", "C2", "Batch A"),
            ("TUE", "14:00", "15:30", "B1 LAB", "Batch B"),
            ("TUE", "15:30", "17:00", "D2", "Batch A"),
            
            # Wednesday
            ("WED", "09:00", "10:00", "C1", "Batch A"),
            ("WED", "10:00", "11:00", "D1", "Batch A"),
            ("WED", "10:30", "11:30", "CS251", "Batch C"),
            ("WED", "11:00", "12:00", "D1", "Batch B"),
            ("WED", "14:00", "15:30", "C2", "Batch A"),
            ("WED", "15:30", "17:00", "D2", "Batch C"),
            
            # Thursday
            ("THU", "09:00", "10:00", "D1", "Batch A"),
            ("THU", "10:00", "11:00", "C1", "Batch A"),
            ("THU", "11:00", "12:15", "B1 TUT", "Batch A"),
            ("THU", "14:00", "15:30", "D2", "Batch B"),
            ("THU", "15:30", "17:00", "C2", "Batch C"),
            
            # Friday
            ("FRI", "09:00", "10:00", "E1", "Batch A"),
            ("FRI", "10:00", "11:00", "B1", "Batch A"),
            ("FRI", "11:00", "12:00", "C1 TUT", "Batch A"),
            ("FRI", "14:00", "15:30", "CS304", "Batch C"),
            ("FRI", "17:30", "18:30", "C2 TUT", "Batch A"),
        ]

    def get_student_timetable(self, student):
        courses = self.students[student]
        data = []
        
        # Day ordering for proper sorting
        day_order = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}
        
        for day, start, end, code, batch in self.timetable:
            if batch != student:
                continue
                
            course_code = code.split()[0]
            if course_code in courses:
                cname = self.courses.get(course_code, {}).get("name", "Unknown")
                room = self.courses.get(course_code, {}).get("room", "TBA")
                faculty = self.courses.get(course_code, {}).get("faculty", "TBA")
                data.append([day, start, end, code, cname, room, faculty, day_order.get(day, 99)])
        
        df = pd.DataFrame(data, columns=["Day", "Start", "End", "Code", "Course", "Room", "Faculty", "DayOrder"])
        # Sort by day order first, then by start time
        df = df.sort_values(["DayOrder", "Start"]).reset_index(drop=True)
        # Remove the helper column
        return df[["Day", "Start", "End", "Code", "Course", "Room", "Faculty"]]


class TimetableScheduler:
    def __init__(self, days=5, slots_per_day=12, rooms=4, faculties=4, courses=6, groups=3, seed=None):
        self.days = days
        self.slots = slots_per_day
        self.num_rooms = rooms
        self.num_faculties = faculties
        self.num_courses = courses
        self.num_groups = groups

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        self.day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][:days]
        self.room_names = [f'Room {chr(65+i)}' for i in range(rooms)]
        self.faculty_names = [f'Dr. {chr(65+i)}' for i in range(faculties)]
        self.course_names = [f'Course {i+1}' for i in range(courses)]
        self.group_names = [f'Batch {chr(65+i)}' for i in range(groups)]

        self._initialize_matrices()

    def _initialize_matrices(self):
        self.schedule = np.zeros((self.days, self.slots, self.num_rooms), dtype=int)
        # Increase faculty availability to 90%
        self.faculty_availability = np.random.choice([0, 1], size=(self.num_faculties, self.days, self.slots), p=[0.1, 0.9])
        # Increase group availability to 95%
        self.group_availability = np.random.choice([0, 1], size=(self.num_groups, self.days, self.slots), p=[0.05, 0.95])

        base_rooms = np.array([
            [60, 0, 1, 1],
            [40, 0, 1, 0],
            [30, 1, 1, 1],
            [25, 1, 0, 0],
        ])
        if self.num_rooms <= base_rooms.shape[0]:
            self.room_properties = base_rooms[:self.num_rooms]
        else:
            extra = np.tile(base_rooms[-1], (self.num_rooms - base_rooms.shape[0], 1))
            self.room_properties = np.vstack([base_rooms, extra])[:self.num_rooms]

        base_courses = np.array([
            [2, 0, 1, 50],
            [3, 0, 1, 40],
            [2, 1, 1, 25],
            [4, 1, 1, 30],
            [2, 0, 0, 35],
            [3, 0, 1, 45],
        ])
        if self.num_courses <= base_courses.shape[0]:
            self.course_requirements = base_courses[:self.num_courses]
        else:
            extra = np.tile(base_courses[-1], (self.num_courses - base_courses.shape[0], 1))
            self.course_requirements = np.vstack([base_courses, extra])[:self.num_courses]

        # Increase faculty-course mapping to 80%
        self.faculty_course_mapping = np.random.choice([0, 1], size=(self.num_faculties, self.num_courses), p=[0.2, 0.8])
        for c in range(self.num_courses):
            if self.faculty_course_mapping[:, c].sum() == 0:
                self.faculty_course_mapping[random.randint(0, self.num_faculties-1), c] = 1

        self.course_group_needs = np.random.randint(2, 6, size=(self.num_courses, self.num_groups))
        self.faculty_workload = np.zeros(self.num_faculties)
        self.scheduled_classes = []

    def check_room_suitable(self, room_idx, course_idx):
        duration, needs_lab, needs_projector, min_capacity = self.course_requirements[course_idx]
        capacity, is_lab, has_projector, has_ac = self.room_properties[room_idx]
        return (capacity >= min_capacity) and (is_lab >= needs_lab) and (has_projector >= needs_projector)

    def find_valid_slots(self, faculty_idx, group_idx, course_idx, duration):
        valid_slots = []
        for day in range(self.days):
            for start_slot in range(self.slots - duration + 1):
                for room in range(self.num_rooms):
                    if not self.check_room_suitable(room, course_idx):
                        continue
                    slot_range = slice(start_slot, start_slot + duration)
                    
                    # Check if room is free
                    room_free = np.all(self.schedule[day, slot_range, room] == 0)
                    if not room_free:
                        continue
                    
                    # Check if faculty is available
                    faculty_free = np.all(self.faculty_availability[faculty_idx, day, slot_range] == 1)
                    if not faculty_free:
                        continue
                    
                    # Check if group is free
                    group_free = np.all(self.group_availability[group_idx, day, slot_range] == 1)
                    if not group_free:
                        continue
                    
                    # Check faculty is not teaching in another room at same time
                    faculty_not_teaching = True
                    for other_room in range(self.num_rooms):
                        if other_room != room:
                            if np.any(self.schedule[day, slot_range, other_room] == (faculty_idx + 100)):
                                faculty_not_teaching = False
                                break
                    
                    if faculty_not_teaching:
                        valid_slots.append((day, start_slot, room))
        return valid_slots

    def schedule_class(self, faculty_idx, group_idx, course_idx, day, start_slot, room, duration):
        self.schedule[day, start_slot:start_slot+duration, room] = faculty_idx + 100
        self.faculty_availability[faculty_idx, day, start_slot:start_slot+duration] = 0
        self.group_availability[group_idx, day, start_slot:start_slot+duration] = 0
        self.faculty_workload[faculty_idx] += duration * 0.5
        self.scheduled_classes.append({
            'faculty': self.faculty_names[faculty_idx],
            'group': self.group_names[group_idx],
            'course': self.course_names[course_idx],
            'day': self.day_names[day],
            'start_slot': start_slot,
            'duration': duration,
            'room': self.room_names[room]
        })

    def generate_timetable(self, max_attempts_per_session=50):
        self.scheduled_classes = []
        self.faculty_workload = np.zeros(self.num_faculties)

        # Process all groups simultaneously to encourage parallel scheduling
        course_priority = sorted(range(self.num_courses), key=lambda c: self.course_requirements[c][1], reverse=True)
        
        # Create a list of all (course, group) pairs
        scheduling_tasks = []
        for course_idx in course_priority:
            for group_idx in range(self.num_groups):
                hours_needed = int(self.course_group_needs[course_idx, group_idx])
                duration = int(self.course_requirements[course_idx][0])
                sessions_needed = int(np.ceil(hours_needed / (duration * 0.5)))
                scheduling_tasks.append((course_idx, group_idx, sessions_needed, duration))
        
        # Shuffle tasks to avoid always prioritizing the same groups
        random.shuffle(scheduling_tasks)
        
        for course_idx, group_idx, sessions_needed, duration in scheduling_tasks:
            eligible_faculty = np.where(self.faculty_course_mapping[:, course_idx] == 1)[0]
            if len(eligible_faculty) == 0:
                continue
            
            scheduled_sessions = 0
            attempts = 0
            
            while scheduled_sessions < sessions_needed and attempts < max_attempts_per_session:
                attempts += 1
                faculty_idx = eligible_faculty[np.argmin(self.faculty_workload[eligible_faculty])]
                valid_slots = self.find_valid_slots(faculty_idx, group_idx, course_idx, duration)
                
                if valid_slots:
                    day, start_slot, room = random.choice(valid_slots)
                    self.schedule_class(faculty_idx, group_idx, course_idx, day, start_slot, room, duration)
                    scheduled_sessions += 1
                else:
                    if len(eligible_faculty) > 1:
                        eligible_faculty = np.delete(eligible_faculty, np.where(eligible_faculty == faculty_idx))
                    else:
                        break
        
        return self.scheduled_classes

    def matrix_for_day(self, day=0):
        return self.schedule[day]
    
    def get_sorted_dataframe(self):
        """Returns a sorted DataFrame with proper day and time ordering"""
        if not self.scheduled_classes:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.scheduled_classes)
        
        # Add numeric day order for sorting
        day_order = {name: i for i, name in enumerate(self.day_names)}
        df['day_order'] = df['day'].map(day_order)
        
        # Convert times
        df['start_time'] = df['start_slot'].apply(lambda s: f"{9 + s//2:02d}:{'00' if s%2==0 else '30'}")
        df['end_time'] = (df['start_slot'] + df['duration']).apply(lambda s: f"{9 + s//2:02d}:{'00' if s%2==0 else '30'}")
        
        # Sort by day, then by start time
        df = df.sort_values(['day_order', 'start_slot']).reset_index(drop=True)
        
        # Return clean columns in logical order
        return df[['day', 'start_time', 'end_time', 'course', 'group', 'faculty', 'room']]


# Main Streamlit App
def main():
    st.set_page_config(page_title='Timetable Dashboard', layout='wide')
    st.title('🎓 Timetable Automation Dashboard')
    st.caption('Advanced schedule management system with realistic course data')

    st.sidebar.header('Quick Controls')
    mode = st.sidebar.selectbox('Mode', ['Student view (static)', 'Auto-scheduler (generate)'])

    if mode == 'Student view (static)':
        st.sidebar.write('Displaying timetable with realistic course data based on university schedule.')
        student_tt = StudentTimetable()
        student_list = list(student_tt.students.keys())
        student = st.sidebar.selectbox('Select student/batch', student_list)
        
        if st.sidebar.button('Show timetable'):
            df = student_tt.get_student_timetable(student)
            st.subheader(f'📅 Timetable for {student}')
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # Display summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Classes", len(df))
                with col2:
                    unique_courses = df['Code'].apply(lambda x: x.split()[0]).nunique()
                    st.metric("Courses", unique_courses)
                with col3:
                    unique_days = df['Day'].nunique()
                    st.metric("Active Days", unique_days)
                
                csv = df.to_csv(index=False)
                st.download_button('📥 Download CSV', csv, file_name=f'{student}_timetable.csv', mime='text/csv')
            else:
                st.info("No classes scheduled for this batch.")

    else:
        st.sidebar.write('Auto-generate a timetable with constraints (experimental).')
        days = st.sidebar.slider('Working days', 3, 5, 5)
        slots_per_day = st.sidebar.slider('Slots per day (30-min)', 6, 20, 12)
        rooms = st.sidebar.slider('Number of rooms', 2, 8, 4)
        faculties = st.sidebar.slider('Number of faculties', 1, 8, 4)
        courses = st.sidebar.slider('Number of courses', 1, 12, 6)
        groups = st.sidebar.slider('Number of student groups', 1, 6, 3)
        seed = st.sidebar.number_input('Random seed (optional)', value=42)

        if st.sidebar.button('Generate timetable'):
            with st.spinner('Generating timetable — optimizing schedule...'):
                sched = TimetableScheduler(
                    days=days, 
                    slots_per_day=slots_per_day, 
                    rooms=rooms, 
                    faculties=faculties, 
                    courses=courses, 
                    groups=groups, 
                    seed=int(seed)
                )
                sched.generate_timetable()

            st.success('✅ Generation complete')
            st.subheader('📊 Scheduled Classes')
            
            if sched.scheduled_classes:
                # Get sorted dataframe
                df = sched.get_sorted_dataframe()
                st.dataframe(df, use_container_width=True)

                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Classes", len(df))
                with col2:
                    st.metric("Avg per Day", f"{len(df)/sched.days:.1f}")
                with col3:
                    utilization = (len(df) / (sched.days * sched.slots * sched.num_rooms)) * 100
                    st.metric("Room Utilization", f"{utilization:.1f}%")
                with col4:
                    st.metric("Active Faculties", (sched.faculty_workload > 0).sum())

                # Export sorted CSV
                csv = df.to_csv(index=False)
                st.download_button('📥 Download schedule CSV', csv, file_name='generated_schedule.csv', mime='text/csv')

                st.subheader('🏢 Room Occupancy Visualization')
                day_idx = st.selectbox('Inspect day matrix', list(range(sched.days)), format_func=lambda x: sched.day_names[x])
                matrix = sched.matrix_for_day(day=day_idx)
                
                fig, ax = plt.subplots(figsize=(10, max(2, sched.slots*0.25)))
                im = ax.imshow(matrix > 0, aspect='auto', cmap='RdYlGn_r')
                ax.set_yticks(range(sched.slots))
                ax.set_yticklabels([f"{9 + s//2}:{'00' if s%2==0 else '30'}" for s in range(sched.slots)])
                ax.set_xticks(range(sched.num_rooms))
                ax.set_xticklabels(sched.room_names)
                ax.set_title(f"Room occupancy — {sched.day_names[day_idx]}")
                plt.tight_layout()
                st.pyplot(fig)

                st.subheader('👨‍🏫 Faculty Workload Distribution')
                fw = pd.DataFrame({'Faculty': sched.faculty_names, 'Hours': np.round(sched.faculty_workload, 2)})
                fw = fw.sort_values('Hours', ascending=False).reset_index(drop=True)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(fw, use_container_width=True)
                with col2:
                    fig2, ax2 = plt.subplots(figsize=(8, 4))
                    ax2.barh(fw['Faculty'], fw['Hours'], color='steelblue')
                    ax2.set_xlabel('Hours')
                    ax2.set_title('Faculty Teaching Hours')
                    plt.tight_layout()
                    st.pyplot(fig2)
            else:
                st.warning('⚠️ No classes could be scheduled. Try adjusting parameters or seed.')

    st.markdown('---')
    st.markdown('**How to run:** `streamlit run app.py`')
    st.markdown('**Features:** Student static view • Auto-scheduler • Visual matrix • Faculty analytics • CSV export')


if __name__ == "__main__":
    main()