from rest_framework import serializers
from .models import TutorVideoPost, TuteeVideoPost, Feedback

class TutorVideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorVideoPost
        fields = ['pk','video_name', 'video', 'thumbnail_img','user','created_at']
        read_only_fields = ['user','created_at']

class TuteeVideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuteeVideoPost
        fields = ['pk','tutee_video','tutor_video']

