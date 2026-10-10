# Student Information System

A command-line Student Information System built with Python. It supports full CRUD, JSON storage, logging, and configuration management.

## Features
- Add, view, update, and delete students
- View a student by ID
- Search students by name, email, or course
- Email validation
- JSON data storage
- Logging to file and console
- External configuration (`config/config.json`)

## Project Structure
    student-info-system/
    ├── src/
    │   ├── models/student.py
    │   ├── services/student_service.py
    │   └── main.py
    ├── data/students.json
    ├── config/config.json
    ├── logs/
    ├── tests/
    ├── README.md
    ├── requirements.txt
    └── .gitignore

## Requirements
- Python 3.8+

## How to Run
From the project root folder:

    python -m src.main

## Usage
Choose an option from the menu (1-7) and follow the prompts.

## Author
Drew Harvey Nikolai A. Gonzales