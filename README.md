# Japanese LMS Backend Assessment

This is the backend implementation for a simplified Japanese Language Learning Management System (LMS), built with Django and Django Rest Framework.

## Features
- User Registration and Token-based Authentication.
- CRUD for Courses and Lessons.
- Custom endpoints to fetch lessons for a course.
- API for quiz submission and score calculation.
- Automatic user progress tracking based on quiz scores.

## Setup Instructions

1. **Clone the repository.**
2. **Create and activate a virtual environment:** `python -m venv venv` then `venv\Scripts\activate` (on Windows).
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Apply database migrations:** `python manage.py migrate`
5. **Create a superuser:** `python manage.py createsuperuser`
6. **Run the server:** `python manage.py runserver`

## API Documentation
The API can be tested using the provided Postman collection file: `Japanese_LMS_API.postman_collection.json`.