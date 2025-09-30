import numpy as np
from typing import List, Dict, Tuple
import random

class TimetableScheduler:
    def __init__(self, days=5, slots_per_day=12, rooms=4, faculties=4, courses=6, groups=3):
        """
        Initialize the multi-dimensional timetable scheduler.
        
        Dimensions:
        - days: Number of working days (default 5)
        - slots_per_day: Number of 30-min time slots per day (default 12 = 6 hours)
        - rooms: Number of available rooms
        - faculties: Number of faculty members
        - courses: Number of courses to schedule
        - groups: Number of student groups/batches
        """
        self.days = days
        self.slots = slots_per_day
        self.num_rooms = rooms
        self.num_faculties = faculties
        self.num_courses = courses
        self.num_groups = groups
        
        # Names for display
        self.day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'][:days]
        self.room_names = [f'Room {chr(65+i)}' for i in range(rooms)]
        self.faculty_names = [f'Dr. {chr(65+i)}' for i in range(faculties)]
        self.course_names = [f'Course {i+1}' for i in range(courses)]
        self.group_names = [f'Batch {chr(65+i)}' for i in range(groups)]
        
        # Initialize matrices
        self._initialize_matrices()
        
    def _initialize_matrices(self):
        """Initialize all constraint matrices"""
        
        # BASE SCHEDULE: [Days × Slots × Rooms] - 0 = free, 1 = occupied
        self.schedule = np.zeros((self.days, self.slots, self.num_rooms), dtype=int)
        
        # FACULTY AVAILABILITY: [Faculties × Days × Slots] - 1 = available, 0 = busy
        # Randomly generate availability (80% available)
        self.faculty_availability = np.random.choice([0, 1], 
                                                     size=(self.num_faculties, self.days, self.slots),
                                                     p=[0.2, 0.8])
        
        # STUDENT GROUP AVAILABILITY: [Groups × Days × Slots] - 1 = available, 0 = busy
        self.group_availability = np.random.choice([0, 1],
                                                   size=(self.num_groups, self.days, self.slots),
                                                   p=[0.15, 0.85])
        
        # ROOM PROPERTIES: [Rooms × Features]
        # Features: [capacity, is_lab, has_projector, has_ac]
        self.room_properties = np.array([
            [60, 0, 1, 1],   # Room A: 60 capacity, lecture hall with projector
            [40, 0, 1, 0],   # Room B: 40 capacity, regular room
            [30, 1, 1, 1],   # Room C: 30 capacity, lab with equipment
            [25, 1, 0, 0],   # Room D: 25 capacity, small lab
        ])
        
        # COURSE REQUIREMENTS: [Courses × Requirements]
        # Requirements: [duration_slots, needs_lab, needs_projector, min_capacity]
        self.course_requirements = np.array([
            [2, 0, 1, 50],   # Course 1: 1 hour, needs projector, 50 students
            [3, 0, 1, 40],   # Course 2: 1.5 hours, needs projector, 40 students
            [2, 1, 1, 25],   # Course 3: 1 hour, needs lab, 25 students
            [4, 1, 1, 30],   # Course 4: 2 hours, needs lab, 30 students
            [2, 0, 0, 35],   # Course 5: 1 hour, simple room, 35 students
            [3, 0, 1, 45],   # Course 6: 1.5 hours, needs projector, 45 students
        ])
        
        # FACULTY-COURSE MAPPING: [Faculties × Courses] - 1 = can teach, 0 = cannot
        self.faculty_course_mapping = np.random.choice([0, 1],
                                                       size=(self.num_faculties, self.num_courses),
                                                       p=[0.3, 0.7])
        # Ensure each course has at least one faculty
        for c in range(self.num_courses):
            if self.faculty_course_mapping[:, c].sum() == 0:
                self.faculty_course_mapping[random.randint(0, self.num_faculties-1), c] = 1
        
        # COURSE-GROUP MAPPING: [Courses × Groups] - hours needed per week
        self.course_group_needs = np.random.randint(2, 6, size=(self.num_courses, self.num_groups))
        
        # FACULTY WORKLOAD TRACKER: [Faculties] - hours scheduled
        self.faculty_workload = np.zeros(self.num_faculties)
        
        # SCHEDULED CLASSES: List to store scheduled classes
        self.scheduled_classes = []
        
    def check_room_suitable(self, room_idx: int, course_idx: int) -> bool:
        """Check if room meets course requirements using matrix operations"""
        duration, needs_lab, needs_projector, min_capacity = self.course_requirements[course_idx]
        capacity, is_lab, has_projector, has_ac = self.room_properties[room_idx]
        
        # Element-wise comparison
        suitable = (
            (capacity >= min_capacity) and
            (is_lab >= needs_lab) and
            (has_projector >= needs_projector)
        )
        return suitable
    
    def find_valid_slots(self, faculty_idx: int, group_idx: int, course_idx: int, duration: int):
        """
        Find all valid time slots using multi-dimensional matrix operations.
        Returns list of (day, start_slot, room) tuples.
        """
        valid_slots = []
        
        for day in range(self.days):
            for start_slot in range(self.slots - duration + 1):
                for room in range(self.num_rooms):
                    # Check if room is suitable for course
                    if not self.check_room_suitable(room, course_idx):
                        continue
                    
                    # Multi-dimensional constraint checking using array slicing
                    slot_range = slice(start_slot, start_slot + duration)
                    
                    # 1. Check room availability (all slots must be free)
                    room_free = np.all(self.schedule[day, slot_range, room] == 0)
                    
                    # 2. Check faculty availability (all slots must be available)
                    faculty_free = np.all(self.faculty_availability[faculty_idx, day, slot_range] == 1)
                    
                    # 3. Check student group availability
                    group_free = np.all(self.group_availability[group_idx, day, slot_range] == 1)
                    
                    # 4. Check faculty not scheduled elsewhere at this time
                    faculty_not_teaching = True
                    for other_room in range(self.num_rooms):
                        if np.any(self.schedule[day, slot_range, other_room] == faculty_idx + 100):
                            faculty_not_teaching = False
                            break
                    
                    # Combined constraint using logical AND
                    if room_free and faculty_free and group_free and faculty_not_teaching:
                        valid_slots.append((day, start_slot, room))
        
        return valid_slots
    
    def schedule_class(self, faculty_idx: int, group_idx: int, course_idx: int, 
                      day: int, start_slot: int, room: int, duration: int):
        """Schedule a class by updating all matrices"""
        
        # Update schedule matrix (mark with faculty ID + 100 to identify who's teaching)
        self.schedule[day, start_slot:start_slot+duration, room] = faculty_idx + 100
        
        # Update faculty availability (mark as busy)
        self.faculty_availability[faculty_idx, day, start_slot:start_slot+duration] = 0
        
        # Update group availability (mark as busy)
        self.group_availability[group_idx, day, start_slot:start_slot+duration] = 0
        
        # Update faculty workload
        self.faculty_workload[faculty_idx] += duration * 0.5  # Convert slots to hours
        
        # Record scheduled class
        self.scheduled_classes.append({
            'faculty': self.faculty_names[faculty_idx],
            'group': self.group_names[group_idx],
            'course': self.course_names[course_idx],
            'day': self.day_names[day],
            'start_slot': start_slot,
            'duration': duration,
            'room': self.room_names[room]
        })
        
    def generate_timetable(self):
        """Generate timetable using backtracking with constraint propagation"""
        
        print("🔄 Generating timetable using multi-dimensional matrices...\n")
        
        # Priority: Schedule courses that need labs first (more constrained)
        course_priority = sorted(range(self.num_courses), 
                               key=lambda c: self.course_requirements[c][1], 
                               reverse=True)
        
        for course_idx in course_priority:
            duration = self.course_requirements[course_idx][0]
            
            # For each group that needs this course
            for group_idx in range(self.num_groups):
                hours_needed = self.course_group_needs[course_idx, group_idx]
                sessions_needed = int(np.ceil(hours_needed / (duration * 0.5)))
                
                # Find eligible faculty for this course
                eligible_faculty = np.where(self.faculty_course_mapping[:, course_idx] == 1)[0]
                
                if len(eligible_faculty) == 0:
                    continue
                
                scheduled_sessions = 0
                attempts = 0
                max_attempts = 20
                
                while scheduled_sessions < sessions_needed and attempts < max_attempts:
                    attempts += 1
                    
                    # Try faculty with least workload first
                    faculty_idx = eligible_faculty[np.argmin(self.faculty_workload[eligible_faculty])]
                    
                    # Find valid slots using matrix operations
                    valid_slots = self.find_valid_slots(faculty_idx, group_idx, course_idx, duration)
                    
                    if valid_slots:
                        # Pick a random valid slot
                        day, start_slot, room = random.choice(valid_slots)
                        
                        # Schedule the class
                        self.schedule_class(faculty_idx, group_idx, course_idx, 
                                          day, start_slot, room, duration)
                        scheduled_sessions += 1
                    else:
                        # Try next faculty
                        if len(eligible_faculty) > 1:
                            eligible_faculty = np.delete(eligible_faculty, 
                                                        np.where(eligible_faculty == faculty_idx))
                        else:
                            break
        
        print(f"✅ Scheduled {len(self.scheduled_classes)} classes\n")
        
    def print_timetable(self):
        """Print the generated timetable"""
        print("=" * 80)
        print("TIMETABLE SUMMARY".center(80))
        print("=" * 80)
        
        for i, cls in enumerate(self.scheduled_classes, 1):
            start_time = f"{9 + cls['start_slot']//2}:{('00' if cls['start_slot']%2==0 else '30')}"
            end_slot = cls['start_slot'] + cls['duration']
            end_time = f"{9 + end_slot//2}:{('00' if end_slot%2==0 else '30')}"
            
            print(f"\n{i}. {cls['course']} - {cls['group']}")
            print(f"   Faculty: {cls['faculty']}")
            print(f"   Time: {cls['day']}, {start_time} - {end_time}")
            print(f"   Room: {cls['room']}")
    
    def print_matrix_stats(self):
        """Print statistics about the matrices"""
        print("\n" + "=" * 80)
        print("MATRIX STATISTICS".center(80))
        print("=" * 80)
        
        print(f"\n📊 Schedule Matrix Shape: {self.schedule.shape}")
        print(f"   Total slots: {self.schedule.size}")
        print(f"   Occupied slots: {np.sum(self.schedule > 0)}")
        print(f"   Utilization: {np.sum(self.schedule > 0) / self.schedule.size * 100:.1f}%")
        
        print(f"\n👨‍🏫 Faculty Workload (hours per week):")
        for i, name in enumerate(self.faculty_names):
            print(f"   {name}: {self.faculty_workload[i]:.1f} hours")
        
        print(f"\n🏫 Room Utilization:")
        for i, name in enumerate(self.room_names):
            occupied = np.sum(self.schedule[:, :, i] > 0)
            total = self.days * self.slots
            print(f"   {name}: {occupied}/{total} slots ({occupied/total*100:.1f}%)")
    
    def export_schedule_matrix(self, day: int = 0):
        """Export schedule matrix for a specific day for visualization"""
        print(f"\n📅 Schedule Matrix for {self.day_names[day]}")
        print("-" * 80)
        
        # Time slots
        print("Time  ", end="")
        for room in self.room_names:
            print(f"{room:12s}", end="")
        print()
        print("-" * 80)
        
        for slot in range(self.slots):
            time = f"{9 + slot//2}:{('00' if slot%2==0 else '30')}"
            print(f"{time:6s}", end="")
            
            for room in range(self.num_rooms):
                val = self.schedule[day, slot, room]
                if val == 0:
                    print("    FREE    ", end="")
                else:
                    faculty_id = val - 100
                    print(f"  {self.faculty_names[faculty_id]:8s}", end="")
            print()


# Example usage
if __name__ == "__main__":
    print("🎓 Multi-Dimensional Timetable Scheduler")
    print("=" * 80)
    
    # Create scheduler
    scheduler = TimetableScheduler(days=5, slots_per_day=12, rooms=4, 
                                   faculties=4, courses=6, groups=3)
    
    # Generate timetable
    scheduler.generate_timetable()
    
    # Print results
    scheduler.print_timetable()
    scheduler.print_matrix_stats()
    
    # Show schedule matrix for Monday
    scheduler.export_schedule_matrix(day=0)
    
    print("\n" + "=" * 80)
    print("✨ Timetable generation complete!")
    print("=" * 80)
