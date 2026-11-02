# OnlineCourse Django Project

A starter Django project for the Coursera OnlineCourse tasks. It includes:
- `Question`, `Choice`, and `Submission` models
- Django admin customizations (`QuestionInline`, `ChoiceInline`, `QuestionAdmin`, `LessonAdmin`)
- Bootstrap course detail template
- Mock exam submission and result views
- URL routes for the exam workflow

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

To populate a demo course, lessons, questions, and choices:
```powershell
python manage.py seed_demo
```
Run this after migrations. You can use the admin to inspect/edit the demo content.

## Files for the Coursera submission

- Task 1: `onlinecourse/models.py`
- Task 2: `onlinecourse/admin.py`
- Task 4: `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
- Task 5: `onlinecourse/views.py`
- Task 6: `onlinecourse/urls.py`

For public GitHub URLs, create a public repository and upload the files. URLs are not public until you publish the repository. Screenshots for Tasks 3 and 7 must be captured from the running application after setup; don't submit example/fabricated screenshots.
