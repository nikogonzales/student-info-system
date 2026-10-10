import json
import os
import logging
from datetime import datetime

from src.models.student import Student

logger = logging.getLogger(__name__)


class StudentService:
    """Handles all reading and writing of student data (no menus here)."""

    def __init__(self, data_file="data/students.json"):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        """Create the data folder and an empty JSON file if missing."""
        folder = os.path.dirname(self.data_file)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump([], f)

    def _load_students(self):
        """Read all students from the file. Returns [] on error."""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Could not load data file: {e}")
            return []

    def _save_students(self, students):
        """Write all students to the file."""
        with open(self.data_file, "w") as f:
            json.dump(students, f, indent=2)

    # CREATE
    def add_student(self, student_data):
        students = self._load_students()
        student = Student(**student_data)
        students.append(student.to_dict())
        self._save_students(students)
        return student.to_dict()

    # READ
    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        for student in self._load_students():
            if student["student_id"] == student_id:
                return student
        return None

    # UPDATE
    def update_student(self, student_id, update_data):
        students = self._load_students()
        for student in students:
            if student["student_id"] == student_id:
                student.update(update_data)
                student["updated_at"] = datetime.now().isoformat()
                self._save_students(students)
                return student
        return None

    # DELETE
    def delete_student(self, student_id):
        students = self._load_students()
        remaining = [s for s in students if s["student_id"] != student_id]
        if len(remaining) == len(students):
            return False
        self._save_students(remaining)
        return True

    # BONUS: SEARCH
    def search_students(self, keyword):
        keyword = keyword.lower()
        return [
            s for s in self._load_students()
            if keyword in s["name"].lower()
            or keyword in s["email"].lower()
            or keyword in s["course"].lower()
        ]