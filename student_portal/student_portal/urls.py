from django.contrib import admin
from django.urls import path, include
from classroom.views import index
from django.conf import settings
from django.conf.urls.static import static
from authy.views import UserProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("authy.urls")),
    path('course/', include("classroom.urls")),
    path('direct/', include("direct.urls")),
    path('', index, name='index'),
    path('<username>/', UserProfile, name="user-profile"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


