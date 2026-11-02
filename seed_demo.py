from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice


class Command(BaseCommand):
    help = "Create a demo course with lessons and mock exam questions."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name="Python Fundamentals",
            defaults={"description": "A short introductory course with a practice mock exam."},
        )
        lesson, _ = Lesson.objects.get_or_create(
            course=course, title="Python Basics",
            defaults={"content": "Review variables, data types, and basic Python syntax.", "order": 1},
        )
        q1, _ = Question.objects.get_or_create(
            lesson=lesson, question_text="Which keyword defines a function in Python?",
            defaults={"grade": 1},
        )
        Choice.objects.get_or_create(question=q1, choice_text="func", defaults={"is_correct": False})
        Choice.objects.get_or_create(question=q1, choice_text="def", defaults={"is_correct": True})
        Choice.objects.get_or_create(question=q1, choice_text="function", defaults={"is_correct": False})

        q2, _ = Question.objects.get_or_create(
            lesson=lesson, question_text="Which data type stores a sequence of characters?",
            defaults={"grade": 1},
        )
        Choice.objects.get_or_create(question=q2, choice_text="str", defaults={"is_correct": True})
        Choice.objects.get_or_create(question=q2, choice_text="int", defaults={"is_correct": False})
        Choice.objects.get_or_create(question=q2, choice_text="bool", defaults={"is_correct": False})

        self.stdout.write(self.style.SUCCESS("Demo course and mock exam data are ready."))
