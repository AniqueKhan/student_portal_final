from django.contrib import admin
from .models import Module
# Register your models here.

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title','user']


admin.site.register(Module,ModuleAdmin)