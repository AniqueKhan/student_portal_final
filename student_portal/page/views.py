from django.shortcuts import render,redirect,get_object_or_404
from .models import Page,PostFileContent
from .forms import NewPage
from django.contrib.auth.decorators import login_required
from classroom.models import Course
from completion.models import Completion
from module.models import Module
from django.http import HttpResponse
# Create your views here.

@login_required
def new_page(request,course_id,module_id):
    user = request.user
    course = get_object_or_404(Course,id=course_id)
    module = get_object_or_404(Module,id=module_id)

    files_objects = []

    if user!=course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")

    else:
        if request.method == "POST":
            form = NewPage(request.POST,request.FILES)
            if form.is_valid():
                title = form.cleaned_data.get("title")
                content = form.cleaned_data.get("content")
                files = request.FILES.getlist('files')

                for file in files:
                    file_instance = PostFileContent(file=file,user=user)
                    file_instance.save()
                    files_objects.append(file_instance)
                
                page = Page.objects.create(title=title,content=content,user=user)
                page.files.set(files_objects)
                page.save()
                module.pages.add(page)
                return redirect("course-modules", course_id=course_id)
        else:
            form = NewPage()
    context = {
        "form":form
    }
    return render(request,"page/new_page.html",context)

def edit_page(request,course_id,module_id,page_id):
    user = request.user
    course = get_object_or_404(Course,id=course_id)
    module = get_object_or_404(Module,id=module_id)
    page = get_object_or_404(Page,id=page_id)
    files_objects = []

    if user!=course.user:
        return HttpResponse("<h1>You are not allowed to perform that operation.</h1>")
    else:
        if request.method == "POST":
            form = NewPage(request.POST,request.FILES,instance=page)
            if form.is_valid():
                page.title = form.cleaned_data.get("title")
                page.content = form.cleaned_data.get("content")
                files = request.FILES.getlist('files')
                print(files)
                print(request.FILES)
                for file in files:
                    file_instance = PostFileContent(file=file,user=user)
                    file_instance.save()
                    files_objects.append(file_instance)
                print(files_objects)
                page.files.set(files_objects)
                page.save()
                module.pages.add(page)
                module.save()
                return redirect("course-modules", course_id=course_id)
        else:
            form = NewPage(instance=page)
    context = {
        "form":form
    }
    return render(request,"page/edit_page.html",context)


def delete_page(request,course_id,module_id,page_id):
    page = get_object_or_404(Page,id=page_id)
    page.delete()
    return redirect("course-modules",course_id=course_id)

def page_detail(request,course_id,module_id,page_id):
    # Passing these args so we can use them in the url
    # No use case of these args in the view
    page = get_object_or_404(Page,id=page_id)
    course = get_object_or_404(Course,id=course_id)
    completed = Completion.objects.filter(user=request.user,course=course,page=page).exists()
    context = {
        'page':page,
        'course':course,
        'completed':completed,
        'module_id':module_id,

    }
    return render(request, "page/page_detail.html",context)

def mark_page_as_done(request,course_id,module_id,page_id):
    page = get_object_or_404(Page,id=page_id)
    course = get_object_or_404(Course,id=course_id)
    Completion.objects.create(page=page,course=course,user=request.user)
    return redirect("course-modules",course_id=course_id)


