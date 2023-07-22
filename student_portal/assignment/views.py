from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Assignment, Submission, AssignmentFileContent
from .forms import NewAssignmentForm, NewSubmissionForm
from module.models import Module
from classroom.models import Course, Grade
from completion.models import Completion

# Create your views here.

def new_assignment(request, course_id, module_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    files_objects = []

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get("title")
                content = form.cleaned_data.get("content")
                points = form.cleaned_data.get("points")
                due = form.cleaned_data.get("due")
                files = request.FILES.getlist('files')
                for file in files:
                    file_instance = AssignmentFileContent(file=file, user=user)
                    file_instance.save()
                    files_objects.append(file_instance)
                assignment = Assignment.objects.create(
                    user=user, title=title, content=content, points=points, due=due)
                assignment.files.set(files_objects)
                assignment.save()
                module.assignments.add(assignment)
                return redirect('course-modules', course_id=course.id)
        else:
            form = NewAssignmentForm()
    context = {
        "form": form
    }
    return render(request, 'assignment/new_assignment.html', context)

def edit_assignment(request, course_id, module_id,assignment_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    files_objects = []

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        if request.method == 'POST':
            form = NewAssignmentForm(request.POST, request.FILES,instance=assignment)
            if form.is_valid():
                assignment.title = form.cleaned_data.get("title")
                assignment.content = form.cleaned_data.get("content")
                assignment.points = form.cleaned_data.get("points")
                assignment.due = form.cleaned_data.get("due")
                files = request.FILES.getlist('files')
                for file in files:
                    file_instance = AssignmentFileContent(file=file, user=user)
                    file_instance.save()
                    files_objects.append(file_instance)
                assignment.files.set(files_objects)
                assignment.save()
                module.assignments.add(assignment)
                return redirect('course-modules', course_id=course.id)
        else:
            form = NewAssignmentForm(instance=assignment)
    context = {
        "form": form
    }
    return render(request, 'assignment/edit_assignment.html', context)


def delete_assignment(request, course_id, module_id,assignment_id):
    course = get_object_or_404(Course, id=course_id)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    assignment.delete()
    return redirect('course-modules', course_id=course.id)
    

def assignment_detail(request, course_id, module_id, assignment_id):
    user = request.user
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = get_object_or_404(Course, id=course_id)
    my_submissions = Submission.objects.filter(
        assignment=assignment, user=user).order_by('-date')
    context = {
        "assignment": assignment,
        "course": course,
        "my_submissions": my_submissions,
        'module_id': module_id,

    }
    return render(request, 'assignment/assignment_detail.html', context)


def submit_assignment(request, course_id, module_id, assignment_id):
    user = request.user
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = NewSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get("file")
            comment = form.cleaned_data.get('comment')
            submission = Submission.objects.create(
                file=file, comment=comment, user=user, assignment=assignment)
            Grade.objects.create(course=course, submission=submission)
            Completion.objects.create(user=user,course=course,assignment=assignment)
            return redirect('assignment-detail', course_id=course_id, module_id=module_id, assignment_id=assignment_id)
    else:
        form = NewSubmissionForm()
    context = {
        "form": form,
        "assignment": assignment
    }
    return render(request, 'assignment/submit_assignment.html', context)
