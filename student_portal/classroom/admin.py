from django.contrib import admin
from .models import Category, Course, Announcement

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')

    list_editable = ['user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.register(Announcement)
