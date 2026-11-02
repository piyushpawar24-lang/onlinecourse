from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Choice, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/course_list.html", {"courses": courses})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Choice, Enrollment, Learner, Question, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect("onlinecourse:course_details", course_id=course.id)

    learner, _ = Learner.objects.get_or_create(user=request.user)
    enrollment, _ = Enrollment.objects.get_or_create(
        learner=learner,
        course=course,
    )

    questions = list(Question.objects.filter(course=course).order_by("id"))
    total = sum(question.grade for question in questions)

    submission = Submission.objects.create(
        enrollment=enrollment,
        score=0,
        total_questions=total,
    )

    score = 0
    selected_choices = []

    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        selected = Choice.objects.filter(
            pk=selected_id,
            question=question,
        ).first() if selected_id else None

        if selected:
            selected_choices.append(selected)
            score += question.is_get_score(selected)

    submission.choices.set(selected_choices)
    submission.score = score
    submission.save(update_fields=["score"])

    return redirect(
        "onlinecourse:show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course,
        enrollment__learner__user=request.user,
    )

    questions = Question.objects.filter(course=course).order_by("id")

    selected_by_question = {
        choice.question_id: choice
        for choice in submission.choices.select_related("question")
    }

    results = []

    for question in questions:
        selected = selected_by_question.get(question.id)
        correct = question.choices.filter(is_correct=True).first()

        results.append({
            "question": question,
            "selected_choice": selected,
            "correct_choice": correct,
            "is_correct": bool(selected and selected.is_correct),
            "grade": question.is_get_score(selected),
        })

    context = {
        "course": course,
        "submission": submission,
        "results": results,
        "score": submission.score,
        "total_questions": submission.total_questions,
    }

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context,
    )
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
