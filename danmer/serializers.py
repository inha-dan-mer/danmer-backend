from rest_framework import serializers
from .models import TutorVideoPost, TuteeVideoPost


class TutorVideoPostSerializer(serializers.ModelSerializer):
    # custom field : must define function (get_name)
    uid = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    tutor_id = serializers.SerializerMethodField()

    class Meta:
        model = TutorVideoPost
        fields = [
            "tutor_id",
            "video_title",
            "video_url",
            "thumbnail_url",
            "song_artist",
            "coordinate_url",
            "uid",
            "username",
        ]
        read_only_fields = ["tutor_id", "coordinate_url", "uid", "username"]

    def get_uid(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_tutor_id(self, obj):
        return obj.id


class NoneFeedbackVideoSerializer(serializers.ModelSerializer):
    tutee_id = serializers.SerializerMethodField()

    class Meta:
        model = TuteeVideoPost
        fields = ["tutee_id"]

    def get_tutee_id(self, obj):
        return obj.id


class TuteeVideoPostSerializer(serializers.ModelSerializer):
    tutor_video_id = serializers.IntegerField()
    uid = serializers.SerializerMethodField()
    tutee_id = serializers.SerializerMethodField()

    class Meta:
        model = TuteeVideoPost
        fields = [
            "tutee_id",
            "tutee_video",
            "tutor_video_id",
            "feedback_result",
            "uid",
        ]
        read_only_fields = ["tutee_id", "uid", "feedback_result"]

    def get_tutee_id(self, obj):
        return obj.id

    def get_uid(self, obj):
        return obj.user.id

    # def get_tutor_video_id(self, obj):
    #     return obj.tutor_video.id


class TutorCoordinateSerializer(serializers.Serializer):
    tutor_id = serializers.IntegerField()
    coordinate_url = serializers.URLField()


class TuteeFeedbackSerializer(serializers.Serializer):
    tutee_id = serializers.IntegerField()
    feedback_result = serializers.JSONField()


# class FeedbackSerializer(serializers.ModelSerializer):
#     #tutee_video_id = serializers.IntegerField()
#     class Meta:
#         model = Feedback
#         fields = ['pk','result_per_part','tutee_video_id']
