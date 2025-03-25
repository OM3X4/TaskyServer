from rest_framework import serializers
from .models import Topic , Task
from django.contrib.auth.models import User


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id" , "name"]

class TaskSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)  # Include topic details
    topic_id = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), source='topic', write_only=True, required=False
    )


    class Meta:
        model = Task
        fields = ["id" , "name" , "status" , "user" , "topic" ,"topic_id" , "expire"]
        read_only_fields = ["user"]