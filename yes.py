# Mini LMS with Teacher & Student Login
# Role-based menu

class Course:
    def __init__(self, title, lessons):
        self.title = title
        self.lessons = lessons
        self.enrolled_students = []           # list of Student objects

class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password              # plain text (for learning only)
        self.completed_lessons = {}           # course_title → lessons_completed

# Global data
courses = []
students = []                                 # list of Student objects
teachers = [
    {"username": "teacher1", "password": "1234"},
    {"username": "admin",    "password": "admin"}
]


def find_student(username):
    for s in students:
        if s.username.lower() == username.lower():
            return s
    return None


def login(role):
    print(f"\n--- {role} Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if role == "Teacher":
        for t in teachers:
            if t["username"] == username and t["password"] == password:
                return {"role": "teacher", "username": username}
        print("Invalid teacher credentials.")
        return None

    elif role == "Student":
        student = find_student(username)
        if student and student.password == password:
            return {"role": "student", "student": student}
        # Auto-register new student if not found (simple approach)
        print("Student not found → creating new account.")
        new_student = Student(username, password)
        students.append(new_student)
        return {"role": "student", "student": new_student}

    return None


def add_course():
    title = input("Enter Course Title: ").strip()
    try:
        lessons = int(input("Enter Number of Lessons: "))
    except ValueError:
        print("Invalid number.")
        return
    if any(c.title.lower() == title.lower() for c in courses):
        print("Course with this title already exists.")
        return
    new_course = Course(title, lessons)
    courses.append(new_course)
    print(f"Course '{title}' added successfully ( {lessons} lessons ).")


def list_courses():
    if not courses:
        print("No courses available yet.")
        return
    print("\nAvailable Courses:")
    for c in courses:
        print(f"• {c.title}  ({c.lessons} lessons)  - Enrolled: {len(c.enrolled_students)}")


def enroll_student(current_student):
    list_courses()
    if not courses:
        return
    title = input("\nEnter course title to enroll: ").strip()
    course = next((c for c in courses if c.title.lower() == title.lower()), None)
    if not course:
        print("Course not found.")
        return
    if current_student in course.enrolled_students:
        print("You are already enrolled in this course.")
        return
    course.enrolled_students.append(current_student)
    print(f"Enrolled successfully in '{course.title}'.")


def complete_lesson(current_student):
    enrolled = [c for c in courses if current_student in c.enrolled_students]
    if not enrolled:
        print("You are not enrolled in any course yet.")
        return

    print("\nYour enrolled courses:")
    for c in enrolled:
        print(f"• {c.title}")

    title = input("\nEnter course title: ").strip()
    course = next((c for c in enrolled if c.title.lower() == title.lower()), None)
    if not course:
        print("Course not found or not enrolled.")
        return

    try:
        done = int(input(f"How many lessons completed (1–{course.lessons}): "))
        if 0 <= done <= course.lessons:
            current_student.completed_lessons[course.title] = done
            print("Progress updated.")
        else:
            print(f"Please enter number between 0 and {course.lessons}.")
    except ValueError:
        print("Invalid number.")


def view_my_progress(current_student):
    enrolled = [c for c in courses if current_student in c.enrolled_students]
    if not enrolled:
        print("You are not enrolled in any course yet.")
        return

    print(f"\nProgress for {current_student.username}:")
    for course in enrolled:
        completed = current_student.completed_lessons.get(course.title, 0)
        total = course.lessons
        perc = (completed / total * 100) if total > 0 else 0
        print(f"• {course.title}:  {completed}/{total} lessons  ({perc:.0f}%)")


def view_course_students():
    list_courses()
    if not courses:
        return
    title = input("\nEnter course title to see enrolled students: ").strip()
    course = next((c for c in courses if c.title.lower() == title.lower()), None)
    if not course:
        print("Course not found.")
        return
    if not course.enrolled_students:
        print("No students enrolled yet.")
        return
    print(f"\nStudents in '{course.title}':")
    for s in course.enrolled_students:
        comp = s.completed_lessons.get(course.title, 0)
        print(f"• {s.username}  - {comp}/{course.lessons} lessons")


def view_student_progress():
    if not students:
        print("No students registered yet.")
        return
    print("\nRegistered students:")
    for s in students:
        print(f"• {s.username}")
    name = input("\nEnter student username: ").strip()
    student = find_student(name)
    if not student:
        print("Student not found.")
        return

    enrolled = [c for c in courses if student in c.enrolled_students]
    if not enrolled:
        print(f"{student.username} is not enrolled in any course.")
        return

    print(f"\nProgress for {student.username}:")
    for course in enrolled:
        comp = student.completed_lessons.get(course.title, 0)
        total = course.lessons
        perc = (comp / total * 100) if total > 0 else 0
        print(f"• {course.title}:  {comp}/{total}  ({perc:.0f}%)")


def teacher_menu():
    while True:
        print("\n┌──────────────────────┐")
        print("│   TEACHER MENU       │")
        print("└──────────────────────┘")
        print("1. Add new course")
        print("2. List all courses")
        print("3. View students in a course")
        print("4. View progress of a student")
        print("0. Logout")
        ch = input("→ ").strip()

        if ch == "1":
            add_course()
        elif ch == "2":
            list_courses()
        elif ch == "3":
            view_course_students()
        elif ch == "4":
            view_student_progress()
        elif ch == "0":
            print("Logged out.\n")
            break
        else:
            print("Invalid choice.")


def student_menu(current_student):
    while True:
        print(f"\n┌────────────────────────────┐")
        print(f"│   WELCOME {current_student.username.upper()}   │")
        print("└────────────────────────────┘")
        print("1. See available courses")
        print("2. Enroll in a course")
        print("3. Mark lessons completed")
        print("4. View my progress")
        print("0. Logout")
        ch = input("→ ").strip()

        if ch == "1":
            list_courses()
        elif ch == "2":
            enroll_student(current_student)
        elif ch == "3":
            complete_lesson(current_student)
        elif ch == "4":
            view_my_progress(current_student)
        elif ch == "0":
            print("Logged out.\n")
            break
        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n" + "═" * 40)
        print("     MINI LEARNING MANAGEMENT SYSTEM")
        print("═" * 40)
        print("1. Teacher Login")
        print("2. Student Login")
        print("0. Exit")
        choice = input("\nSelect option → ").strip()

        if choice == "0":
            print("Thank you! Goodbye.")
            break

        elif choice == "1":
            session = login("Teacher")
            if session:
                teacher_menu()

        elif choice == "2":
            session = login("Student")
            if session:
                student_menu(session["student"])

        else:
            print("Please choose 1, 2 or 0.")


if __name__ == "__main__":
    main()