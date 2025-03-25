from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Topic , Task
from .serializers import TopicSerializer , TaskSerializer

# Create your views here.
@api_view(["GET" , "POST"])
# @permission_classes([IsAuthenticated])
def tasksCreateList(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user).select_related("topic" , "user")
        serial = TaskSerializer(tasks , many=True)
        return Response(serial.data , status=status.HTTP_200_OK)
    elif request.method == "POST":
        serial = TaskSerializer(data=request.data)
        if serial.is_valid():
            topic = serial.validated_data.get("topic" , None)
            if topic and topic.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serial.save(user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET" , "POST"])
# @permission_classes([IsAuthenticated])
def topicListCreate(request):
    if request.method == "GET":
        topics = Topic.objects.filter(user=request.user)
        serial = TopicSerializer(topics , many=True)
        return Response(serial.data , status=status.HTTP_200_OK)
    elif request.method == "POST":
        serial = TopicSerializer(request.data)
        if serial.is_valid():
            serial.save(user=request.user)
            return Response(serial.data , status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
