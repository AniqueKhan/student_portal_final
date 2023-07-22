from django.urls import path
from .views import *
from module.views import *
from page.views import *
from quiz.views import *
from assignment.views import *
from question.views import *

urlpatterns = [
    # Course - Classroom Views
    path("new_course/", new_course, name='new-course'),
    path("browse_courses/", browse_courses, name='browse-courses'),
    path("course_about/<course_id>/", course_about, name='course-about'),
    path("course_detail/<course_id>/", course_detail, name='course-detail'),
    path("categories/", categories, name='categories'),
    path("my_courses/", my_courses, name='my-courses'),
    path("categories/<category_slug>", category_courses, name='category-courses'),
    path("<course_id>/edit", edit_course, name='edit-course'),
    path("<course_id>/enroll", enroll, name='enroll'),
    path("<course_id>/unenroll", unenroll, name='unenroll'),
    path("<course_id>/delete", delete_course, name='delete-course'),
    path("<course_id>/new_announcement",new_announcement,name='new-announcement'),

    # Submission - Classroom Views
    path("<course_id>/my_submissions", my_submissions, name='my-submissions'),
    path("<course_id>/student_submissions",
         student_submissions, name='student-submissions'),
    path("<course_id>/submissions/<grade_id>",
         grade_submission, name='grade-submission'),

    # Module Views
    path("<course_id>/modules", course_modules, name="course-modules"),
    path("<course_id>/modules/new_module", new_module, name="new-module"),
    path("<course_id>/modules/<module_id>/edit", edit_module, name="edit-module"),

    # Page Views
    path("<course_id>/modules/<module_id>/pages/new_page",
         new_page, name='new-page'),
    path("<course_id>/modules/<module_id>/pages/<page_id>",
         page_detail, name='page-detail'),
     path("<course_id>/modules/<module_id>/pages/<page_id>/edit",
         edit_page, name='edit-page'),
     path("<course_id>/modules/<module_id>/pages/<page_id>/delete",
         delete_page, name='delete-page'),
     path("<course_id>/modules/<module_id>/pages/<page_id>/mark_as_done",
         mark_page_as_done, name='mark-page-as-done'),

    # Quiz Views
    path("<course_id>/modules/<module_id>/quizzes/new_quiz",
         new_quiz, name='new-quiz'),
     path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/edit",
         edit_quiz, name='edit-quiz'),
     path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/delete",
         delete_quiz, name='delete-quiz'),
    path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/questions/new_question",
         new_question, name='new-question'),
    path("<course_id>/modules/<module_id>/quizzes/<quiz_id>",
         quiz_detail, name='quiz-detail'),
    path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/take_quiz",
         take_quiz, name='take-quiz'),
    path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/submit_quiz",
         submit_quiz, name='submit-quiz'),
    path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/attempts/<attempt_id>",
         attempt_detail, name='attempt-detail'),
     path("<course_id>/modules/<module_id>/quizzes/<quiz_id>/mark_as_done",
         mark_quiz_as_done, name='mark-quiz-as-done'),

    # Assignment Views
    path("<course_id>/modules/<module_id>/assignments/new_assignment",
         new_assignment, name='new-assignment'),
     path("<course_id>/modules/<module_id>/assignments/<assignment_id>/edit",
         edit_assignment, name='edit-assignment'),
     path("<course_id>/modules/<module_id>/assignments/<assignment_id>/delete",
         delete_assignment, name='delete-assignment'),
    path("<course_id>/modules/<module_id>/assignments/<assignment_id>",
         assignment_detail, name='assignment-detail'),
    path("<course_id>/modules/<module_id>/assignments/<assignment_id>/submit_assignment",
         submit_assignment, name='submit-assignment'),

    # Question Views
    path("<course_id>/questions", course_questions, name='course-questions'),
    path("<course_id>/new_question", new_course_question,
         name='new-course-question'),
    path("<course_id>/questions/<question_id>",
         course_question_detail, name='course-question-detail'),
    path("<course_id>/questions/<question_id>/<answer_id>",
         mark_answer, name='mark-answer'),
    path("<course_id>/questions/<question_id>/<answer_id>/up_vote",
         up_vote, name='up-vote'),
    path("<course_id>/questions/<question_id>/<answer_id>/down_vote",
         down_vote, name='down-vote'),


]
