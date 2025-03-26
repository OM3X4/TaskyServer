from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Topic , Task
from .serializers import TopicSerializer , TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests

googleClientId = "441640127193-68e3tk5smeclt6esno0s311ptlrb1hs1.apps.googleusercontent.com"

# Create your views here.
@api_view(["GET" , "POST"])
@permission_classes([IsAuthenticated])
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
                return Response({"message" : "This Is Not Your Habit"} , status=status.HTTP_403_FORBIDDEN)
            serial.save(user=request.user)

            tasks = Task.objects.filter(user=request.user).select_related("topic" , "user")
            serial = TaskSerializer(tasks , many=True)

            return Response(serial.data  ,status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET" , "POST"])
@permission_classes([IsAuthenticated])
def topicListCreate(request):
    if request.method == "GET":
        topics = Topic.objects.filter(user=request.user)
        serial = TopicSerializer(topics , many=True)
        return Response(serial.data , status=status.HTTP_200_OK)
    elif request.method == "POST":
        serial = TopicSerializer(data=request.data)
        if serial.is_valid():
            serial.save(user=request.user)
            return Response(serial.data , status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggleTask(request, pk):
    try:
        task = Task.objects.get(pk=pk , user=request.user)
    except Task.DoesNotExist:
        return Response({"message": "This Task Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)

    # Toggle the status
    task.status = not task.status
    task.save()

    # Serialize all tasks for the current user
    tasks = Task.objects.filter(user=request.user)
    serial = TaskSerializer(tasks, many=True)  # ✅ Corrected serialization

    return Response(serial.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get("email")
    password = request.data.get("password")

    if not password or not email or not username:
        return Response({"message": "All Fields Are Required"} , status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"message": "This username is Already Taken"} , status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"message": "This email Already Taken"} , status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        "message":  "User Created Successfully",
        "access": str(refresh.access_token),
        'refresh': str(refresh)
    } , status=status.HTTP_201_CREATED)


@api_view(["POST"])
def googleAuth(request):
    token = request.data.get("token")

    if not token:
        return Response({"message" : "Missing Token"} , status=status.HTTP_400_BAD_REQUEST)


    try:
        google_user = id_token.verify_oauth2_token(token , requests.Request() ,googleClientId )

        user, created = User.objects.get_or_create(
                                            email=google_user["email"],
                                            defaults={
                                                "username": google_user["email"],
                                                "first_name": google_user.get("given_name", ""),
                                                "last_name": google_user.get("family_name", ""),
                                            }
                                        )

        refresh = RefreshToken.for_user(user)
        return Response({"access" :str(refresh.access_token) , "refresh": str(refresh)})


    except ValueError:
        return Response({"error": "Invalid token"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)