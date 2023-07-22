from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from .forms import NewQuestionForm, NewQuizForm
from module.models import Module
from completion.models import Completion
from classroom.models import Course


# Create your views here.
def new_quiz(request, course_id, module_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id)
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")

    if request.method == "POST":
        form = NewQuizForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get('content')
            due = form.cleaned_data.get('due')
            allowed_attempts = form.cleaned_data.get('allowed_attempts')
            quiz = Quiz.objects.create(user=user, title=title, content=content, due=due,
                                       allowed_attempts=allowed_attempts)
            module.quizzes.add(quiz)
            module.save()
            return redirect('new-question', course_id=course_id, module_id=module_id, quiz_id=quiz.id)
    else:
        form = NewQuizForm()
    context = {
        "form": form
    }
    return render(request, 'quiz/new_quiz.html', context)

def edit_quiz(request, course_id, module_id,quiz_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id)
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    if request.method == "POST":
        form = NewQuizForm(request.POST,instance=quiz)
        if form.is_valid():
            quiz.title = form.cleaned_data.get("title")
            quiz.content = form.cleaned_data.get('content')
            quiz.due = form.cleaned_data.get('due')
            quiz.allowed_attempts = form.cleaned_data.get('allowed_attempts')
            quiz.save()
            module.quizzes.add(quiz)
            module.save()
            return redirect('course-modules', course_id=course_id)
    else:
        form = NewQuizForm(instance=quiz)
    context = {
        "form": form
    }
    return render(request, 'quiz/edit_quiz.html', context)
    
def delete_quiz(request, course_id, module_id,quiz_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    quiz.delete()
    return redirect('course-modules', course_id=course_id)


def new_question(request, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            points = form.cleaned_data.get('points')
            answer_text = request.POST.getlist('answer_text')
            is_correct = request.POST.getlist('is_correct')
            question = Question.objects.create(
                question_text=question_text, points=points, user=user)
            for a, c in zip(answer_text, is_correct):
                answer = Answer.objects.create(
                    answer_text=a, is_correct=c, user=user)
                question.answers.add(answer)
                question.save()
                quiz.questions.add(question)
                quiz.save()
            return redirect('course-modules', course_id=course_id)
    else:
        form = NewQuestionForm()
    context = {
        "form": form
    }
    return render(request, 'quiz/new_question.html', context)


def quiz_detail(request, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course = get_object_or_404(Course, id=course_id)
    my_attempts = Attempter.objects.filter(quiz=quiz, user=user)
    context = {
        "my_attempts": my_attempts,
        "quiz": quiz,
        "course":course,
        "module_id": module_id
    }
    return render(request, 'quiz/quiz_detail.html', context)


def take_quiz(request, course_id, module_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        "quiz": quiz,
        "course_id": course_id,
        "module_id": module_id
    }
    return render(request, 'quiz/take_quiz.html', context)


def submit_quiz(request, course_id, module_id, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    earned_point = 0
    if request.method == 'POST':
        questions = request.POST.getlist("question")
        answers = request.POST.getlist("answer")
        attempter = Attempter.objects.create(user=user, quiz=quiz, score=0)

        for q, a in zip(questions, answers):
            question = Question.objects.get(id=q)
            answer = Answer.objects.get(id=a)
            Attempt.objects.create(
                quiz=quiz, attempter=attempter, question=question, answer=answer)
            Completion.objects.create(user=user,course_id=course_id,quiz=quiz)
            if answer.is_correct:
                earned_point += question.points
                attempter.score = earned_point
                attempter.save()

        return redirect('quiz-detail', course_id=course_id, module_id=module_id, quiz_id=quiz_id)


def attempt_detail(request, course_id, module_id, quiz_id, attempt_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = Attempt.objects.filter(quiz=quiz, attempter__user=user)

    context = {
        'quiz': quiz,
        'attempts': attempts,
    }
    return render(request, 'quiz/attempt_detail.html', context)

def mark_quiz_as_done(request,course_id,module_id,quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)
    course = get_object_or_404(Course,id=course_id)
    Completion.objects.create(quiz=quiz,course=course,user=request.user)
    return redirect("course-modules",course_id=course_id)