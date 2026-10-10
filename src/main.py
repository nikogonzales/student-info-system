import json
import logging
import os

from src.services.student_service import StudentService


def load_config(path="config/config.json"):
    """Load settings from the config file, with safe defaults."""
    defaults = {
        "data_file": "data/students.json",
        "log_file": "logs/app.log",
        "log_level": "INFO",
    }
    try:
        with open(path, "r") as f:
            defaults.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        print("Config not found or invalid. Using defaults.")
    return defaults


def setup_logging(config):
    """Log to both a file and the console."""
    os.makedirs(os.path.dirname(config["log_file"]), exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, config["log_level"], logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(config["log_file"]),
            logging.StreamHandler(),
        ],
    )


def is_valid_email(email):
    """BONUS: simple data validation."""
    return "@" in email and "." in email.split("@")[-1]


class StudentInformationSystem:
    def __init__(self):
        self.config = load_config()
        setup_logging(self.config)
        self.student_service = StudentService(self.config["data_file"])
        self.logger = logging.getLogger(__name__)

    def display_menu(self):
        print("\n=== Student Information System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Search Students")
        print("7. Exit")

    def print_student(self, s):
        print(f"ID: {s['student_id']}, Name: {s['name']}, "
              f"Email: {s['email']}, Course: {s['course']}, "
              f"Year: {s['year_level']}")

    def add_student(self):
        print("\n--- Add New Student ---")
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        course = input("Course: ").strip()
        year_level = input("Year Level: ").strip()

        if not name or not course or not year_level:
            print("All fields are required.")
            return
        if not is_valid_email(email):
            print("Invalid email address.")
            return

        try:
            student = self.student_service.add_student({
                "name": name, "email": email,
                "course": course, "year_level": year_level,
            })
            self.logger.info(f"Added student: {student['student_id']}")
            print(f"Student added successfully! ID: {student['student_id']}")
        except Exception as e:
            self.logger.error(f"Error adding student: {e}")
            print("Error adding student.")

    def view_all_students(self):
        print("\n--- All Students ---")
        students = self.student_service.get_all_students()
        if not students:
            print("No students found.")
            return
        for s in students:
            self.print_student(s)

    def view_student(self):
        student_id = input("Enter Student ID: ").strip()
        student = self.student_service.get_student(student_id)
        if student:
            print("\nStudent Details:")
            for key, value in student.items():
                print(f"  {key}: {value}")
        else:
            print("Student not found.")

    def update_student(self):
        student_id = input("Enter Student ID to update: ").strip()
        if not self.student_service.get_student(student_id):
            print("Student not found.")
            return

        print("Leave a field blank to keep the current value.")
        fields = {
            "name": input("New name: ").strip(),
            "email": input("New email: ").strip(),
            "course": input("New course: ").strip(),
            "year_level": input("New year level: ").strip(),
        }
        update_data = {k: v for k, v in fields.items() if v}

        if "email" in update_data and not is_valid_email(update_data["email"]):
            print("Invalid email address.")
            return

        try:
            self.student_service.update_student(student_id, update_data)
            self.logger.info(f"Updated student: {student_id}")
            print("Student updated successfully!")
        except Exception as e:
            self.logger.error(f"Error updating student: {e}")
            print("Error updating student.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ").strip()
        confirm = input(f"Delete {student_id}? (y/n): ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return
        try:
            if self.student_service.delete_student(student_id):
                self.logger.info(f"Deleted student: {student_id}")
                print("Student deleted successfully!")
            else:
                print("Student not found.")
        except Exception as e:
            self.logger.error(f"Error deleting student: {e}")
            print("Error deleting student.")

    def search_students(self):
        keyword = input("Search keyword: ").strip()
        results = self.student_service.search_students(keyword)
        if not results:
            print("No matches found.")
            return
        for s in results:
            self.print_student(s)

    def run(self):
        actions = {
            "1": self.add_student,
            "2": self.view_all_students,
            "3": self.view_student,
            "4": self.update_student,
            "5": self.delete_student,
            "6": self.search_students,
        }
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-7): ").strip()
            if choice == "7":
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = StudentInformationSystem()
    app.run()