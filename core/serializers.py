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
        queryset=Topic.objects.all(), source='topic', write_only=True, required=False  # Make topic_id optional
    )

    class Meta:
        model = Task
        fields = ["id", "name", "status", "user", "topic", "topic_id", "expire"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        topic = validated_data.pop('topic', None)  # Extract topic if provided
        task = Task.objects.create(**validated_data)
        if topic:  # Only assign if topic is provided
            task.topic = topic
            task.save()
        return task
