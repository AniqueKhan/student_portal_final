from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from classroom.models import Course
from .forms import *
from .models import *
from django.http import  HttpResponse, HttpResponseRedirect
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

# Create your views here.


def new_course_question(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CourseQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            body = form.cleaned_data.get("body")
            question = CourseQuestion.objects.create(
                title=title, body=body, user=user)
            course.questions.add(question)
            course.save()
            return redirect("course-questions", course_id=course_id)
    else:
        form = CourseQuestionForm()
    context = {
        "form": form,
    }
    return render(request, 'question/new_course_question.html', context)


def course_questions(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = course.questions.all().order_by("-created_at")

    # Pagination

    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    # Paginate items
    questions_per_page = 3
    paginator = Paginator(questions, questions_per_page)

    try:
        questions_page = paginator.page(page)
    except PageNotAnInteger:
        questions_page = paginator.page(default_page)
    except EmptyPage:
        questions_page = paginator.page(paginator.num_page)

    context = {
        "questions_page": questions_page,
        "course": course,
    }
    return render(request, 'question/course_questions.html', context)


def course_question_detail(request, course_id, question_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    question = get_object_or_404(CourseQuestion, id=question_id)
    answers = CourseAnswer.objects.filter(
        question=question).order_by("-is_accepted_answer", "-up_votes", 'down_votes')

    # The moderators are going to be the course teacher and student that asked that question
    moderator = False
    if user == course.user or user == question.user:
        moderator = True

    if request.method == "POST":
        form = CourseAnswerForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get("body")
            CourseAnswer.objects.create(
                user=user, question=question, body=body)
            return redirect("course-question-detail", course_id=course_id, question_id=question_id)
    else:
        form = CourseAnswerForm()
    context = {
        "answers": answers,
        "form": form,
        "question": question,
        'moderator': moderator,
        'course': course
    }
    return render(request, 'question/course_question_detail.html', context)


def mark_answer(request, course_id, question_id, answer_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    question = get_object_or_404(CourseQuestion, id=question_id)

    if user != course.user and user != question.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        answer = get_object_or_404(CourseAnswer, id=answer_id)
        answer.is_accepted_answer = True
        question.has_accepted_answer = True
        answer.save()
        question.save()
        return redirect("course-question-detail", course_id=course_id, question_id=question.id)


def up_vote(request, course_id, question_id, answer_id):
    user = request.user
    answer = get_object_or_404(CourseAnswer, id=answer_id)
    current_votes = answer.up_votes

    up_voted = UpVote.objects.filter(answer=answer, user=user)

    if not up_voted:
        UpVote.objects.create(answer=answer, user=user)
        current_votes += 1
    else:
        UpVote.objects.filter(answer=answer, user=user).delete()
        current_votes -= 1
    answer.up_votes = current_votes
    answer.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def down_vote(request, course_id, question_id, answer_id):
    user = request.user
    answer = get_object_or_404(CourseAnswer, id=answer_id)
    current_votes = answer.down_votes

    down_voted = DownVote.objects.filter(answer=answer, user=user)

    if not down_voted:
        DownVote.objects.create(answer=answer, user=user)
        current_votes += 1
    else:
        DownVote.objects.filter(answer=answer, user=user).delete()
        current_votes -= 1
    answer.down_votes = current_votes
    answer.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
