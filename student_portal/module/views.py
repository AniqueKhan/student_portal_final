from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewModuleForm
from .models import Module
from classroom.models import Course
from completion.models import Completion
from django.http import HttpResponse


# Create your views here.

def new_module(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:

        if request.method == "POST":
            form = NewModuleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get("title")
                description = form.cleaned_data.get("description")
                module = Module.objects.create(
                    title=title, user=user, description=description)
                course.modules.add(module)
                course.save()
                return redirect('course-modules', course_id=course_id)
        else:
            form = NewModuleForm()
        context = {
            "form": form
        }
        return render(request, 'module/new_module.html', context)


def edit_module(request, course_id, module_id):
    user = request.user
    module = get_object_or_404(Module, id=module_id)
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:

        if request.method == "POST":
            form = NewModuleForm(request.POST, instance=module)
            if form.is_valid():
                module.title = form.cleaned_data.get("title")
                module.description = form.cleaned_data.get("description")
                module.save()
                course.save()
                return redirect('course-modules', course_id=course_id)
        else:
            form = NewModuleForm(instance=module)
    context = {
        "form": form,
    }
    return render(request, 'module/edit_module.html', context)


def course_modules(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    page_completions = Completion.objects.filter(
        user=user, course=course).values_list("page__pk", flat=True)
    quiz_completions = Completion.objects.filter(
        user=user, course=course).values_list("quiz__pk", flat=True)
    assignment_completions = Completion.objects.filter(
        user=user, course=course).values_list("assignment__pk", flat=True)

    teacher_mode = False

    if user == course.user:
        teacher_mode = True
    context = {
        "course": course,
        "teacher_mode": teacher_mode,
        "page_completions": page_completions,
        "quiz_completions": quiz_completions,
        "assignment_completions": assignment_completions,
    }
    return render(request, "module/modules.html", context)
