from django.urls import path
from authy.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile

from django.contrib.auth import views as authViews

urlpatterns = [
    path('profile/edit', EditProfile, name='edit-profile'),
    path('signup/', Signup, name='signup'),
    path('login/', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    path('changepassword/', PasswordChange, name='change-password'),
    path('changepassword/done', PasswordChangeDone, name='change-password-done'),
]
