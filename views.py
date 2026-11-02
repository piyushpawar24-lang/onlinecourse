from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Choice, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method != "POST":
        return redirect("onlinecourse:course_details", course_id=course.id)

    questions = [q for lesson in course.lessons.all() for q in lesson.questions.all()]
    score = 0
    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        if selected_id:
            selected = Choice.objects.filter(pk=selected_id, question=question).first()
            if selected and selected.is_correct:
                score += question.grade

    total = sum(question.grade for question in questions)
    submission = Submission.objects.create(
        student=request.user if request.user.is_authenticated else None,
        course=course,
        score=score,
        total_questions=total,
    )
    messages.success(request, "Your mock exam has been submitted.")
    return redirect("onlinecourse:show_exam_result", submission_id=submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    return render(request, "onlinecourse/exam_result.html", {"submission": submission})
