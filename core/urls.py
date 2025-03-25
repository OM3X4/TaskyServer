from django.urls import path
from .views import topicListCreate , tasksCreateList

urlpatterns = [
    path('topics/', topicListCreate, name='topic_list_create'),
    path('tasks/', tasksCreateList, name='todo_list_create'),

]

