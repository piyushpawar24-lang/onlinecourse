from django.conf import settings
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)
    social_link = models.URLField(blank=True)

    def __str__(self):
        return self.user.get_username()


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    instructors = models.ManyToManyField(Instructor, related_name="courses", blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    learner = models.ForeignKey(
        Learner, related_name="enrollments", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="enrollments", on_delete=models.CASCADE
    )
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("learner", "course")

    def __str__(self):
        return f"{self.learner} - {self.course}"


class Question(models.Model):
    course = models.ForeignKey(
        Course, related_name="questions", on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson, related_name="questions", on_delete=models.CASCADE,
        null=True, blank=True
    )
    question_text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=1)

    def is_get_score(self, selected_choice):
        if selected_choice and selected_choice.is_correct:
            return self.grade
        return 0

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, related_name="submissions", on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice, related_name="submissions", blank=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        if not self.total_questions:
            return 0
        return round((self.score / self.total_questions) * 100, 1)

    def __str__(self):
        return f"Submission {self.pk}: {self.score}/{self.total_questions}"
