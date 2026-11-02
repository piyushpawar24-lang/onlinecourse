from django.contrib import admin
from .models import (
    Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "lesson", "grade")
    search_fields = ("question_text",)
    list_filter = ("course", "lesson")
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "enrollment", "score", "total_questions", "submitted_at"
    )
    readonly_fields = ("submitted_at",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("learner", "course", "date_enrolled")
    readonly_fields = ("date_enrolled",)
