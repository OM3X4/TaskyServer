from django.contrib import admin
from .models import Topic , Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Topic)