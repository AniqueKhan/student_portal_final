from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewCourseForm,NewAnnouncementForm
from .models import Course, Category, Grade,Announcement
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


# Create your views here.
@login_required
def index(request):
    user = request.user
    courses = Course.objects.filter(enrolled=user).order_by('-created_at')

    # Pagination

    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    # Paginate items
    courses_per_page = 6
    paginator = Paginator(courses, courses_per_page)

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        courses_page = paginator.page(default_page)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_page)

    context = {
        'courses_page': courses_page,
    }
    return render(request, 'index.html', context)


def categories(request):
    categories = Category.objects.all().annotate(
        course_count=Count('course')).order_by('-course_count')
    context = {
        "categories": categories,
    }
    return render(request, 'classroom/categories.html', context)


def category_courses(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category).order_by('-created_at')

    # Pagination

    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    # Paginate items
    courses_per_page = 3
    paginator = Paginator(courses, courses_per_page)

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        courses_page = paginator.page(default_page)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_page)

    enrolled_courses = Course.objects.filter(enrolled=request.user)
    context = {
        'courses_page': courses_page,
        "category": category,
        "enrolled_courses": enrolled_courses,
    }
    return render(request, 'classroom/category_courses.html', context)


@login_required
def new_course(request):
    user = request.user
    if request.method == "POST":
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            syllabus = form.cleaned_data.get('syllabus')
            category = form.cleaned_data.get('category')
            Course.objects.create(picture=picture, title=title, description=description, syllabus=syllabus,
                                  category=category, user=user)
            return redirect('my-courses')
    else:
        form = NewCourseForm()
    context = {
        'form': form,
    }
    return render(request, 'classroom/new_course.html', context)


def browse_courses(request):
    courses = Course.objects.exclude(
        enrolled=request.user).order_by('-created_at')

    # Pagination

    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    # Paginate items
    courses_per_page = 6
    paginator = Paginator(courses, courses_per_page)

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        courses_page = paginator.page(default_page)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_pages)

    context = {
        'courses_page': courses_page,
    }
    return render(request, 'classroom/browse_courses.html', context)


@login_required
def course_about(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    context = {
        "course": course,
    }
    return render(request, 'classroom/course_about.html', context)


def course_detail(request, course_id):
    user = request.user
    teacher_mode = False
    course = get_object_or_404(Course, id=course_id)
    if not Course.objects.filter(enrolled=user).exists() and not user==course.user:
        return HttpResponse("<h1>You are not allowed to view details of the course until you enrolled in it </h1>")
    
    if user == course.user:
        teacher_mode = True
    context = {
        "course": course,
        "teacher_mode": teacher_mode,
    }
    return render(request, 'classroom/course_detail.html', context)


@login_required
def enroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.add(user)
    return redirect('index')


def unenroll(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    course.enrolled.remove(user)
    return redirect('index')


@login_required
def delete_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        course.delete()
    return redirect('my-courses')


@login_required
def edit_course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        if request.method == "POST":
            # The instance arg pre-populates the fields
            # So we do not need to create a seperate edit course form
            form = NewCourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                course.title = form.cleaned_data.get('title')
                course.picture = form.cleaned_data.get('picture')
                course.description = form.cleaned_data.get('description')
                course.category = form.cleaned_data.get('category')
                course.syllabus = form.cleaned_data.get('syllabus')
                course.save()
                return redirect('my-courses')
        else:
            form = NewCourseForm(instance=course)

    context = {
        "form": form,
        'course': course,
    }
    return render(request, 'classroom/edit_course.html', context)

def new_announcement(request,course_id):
    course = get_object_or_404(Course,id=course_id)
    if request.method == "POST":
        form = NewAnnouncementForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get("body")
            announcement = Announcement.objects.create(body=body)
            announcement.save()
            course.announcements.add(announcement)
            course.save()
            return redirect("course-detail",course_id=course_id)
    else:
        form = NewAnnouncementForm()
    context = {
        "form":form,
    }
    return render(request, "classroom/new_announcement.html",context)




@login_required
def my_courses(request):
    courses = Course.objects.filter(user=request.user).order_by('-created_at')
    # Pagination

    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    # Paginate items
    courses_per_page = 6
    paginator = Paginator(courses, courses_per_page)

    try:
        courses_page = paginator.page(page)
    except PageNotAnInteger:
        courses_page = paginator.page(default_page)
    except EmptyPage:
        courses_page = paginator.page(paginator.num_page)
    context = {
        'courses_page': courses_page,
    }
    return render(request, 'classroom/my_courses.html', context)


# Submission Views
def my_submissions(request, course_id):
    # for the students
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grades = Grade.objects.filter(course=course, submission__user=user)

    context = {
        "course": course,
        "grades": grades
    }
    return render(request, 'classroom/my_submissions.html', context)


def student_submissions(request, course_id):
    # for the teacher
    course = get_object_or_404(Course, id=course_id)
    grades = Grade.objects.filter(course=course).order_by('-submission__date')

    context = {
        "course": course,
        "grades": grades
    }
    return render(request, 'classroom/student_submissions.html', context)


def grade_submission(request, course_id, grade_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    grade = get_object_or_404(Grade, id=grade_id)

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        if request.method == 'POST':
            points = request.POST.get("points")
            grade.points = points
            grade.status = "graded"
            grade.graded_by = user
            grade.save()
            return redirect("student-submissions", course_id=course.id)
    context = {
        "course": course,
        "grade": grade
    }
    return render(request, 'classroom/grade_submissions.html', context)


