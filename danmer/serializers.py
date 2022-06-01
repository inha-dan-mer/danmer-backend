from rest_framework import serializers
from .models import TutorVideoPost, TuteeVideoPost, Feedback

class TutorVideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorVideoPost
        fields = ['pk','video_name', 'video', 'thumbnail_img','user','created_at','singer']
        read_only_fields = ['user','created_at']

class TuteeVideoPostSerializer(serializers.ModelSerializer):
    tutor_video_id = serializers.IntegerField()
    # tutor_video_id = serializers.SerializerMethodField()
    class Meta:
        model = TuteeVideoPost
        fields = ['pk','tutee_video', 'tutor_video_id', 'tutor_video','user']
        read_only_fields = ['tutor_video','user']


class FeedbackSerializer(serializers.ModelSerializer):
    #tutee_video_id = serializers.IntegerField()
    class Meta:
        model = Feedback
        fields = ['pk','result_per_part','tutee_video_id']