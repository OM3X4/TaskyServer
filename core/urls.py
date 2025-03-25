from django.urls import path
from .views import topicListCreate , tasksCreateList , register , googleAuth , toggleTask


urlpatterns = [
    path('topics/', topicListCreate, name='topic_list_create'),
    path('tasks/', tasksCreateList, name='todo_list_create'),
    path("register/" , register , name="Register"),
    path("toggle/<int:pk>/" , toggleTask , name="ToggleTask"),
    path("auth/google/" , googleAuth , name="googleAuth")
]

