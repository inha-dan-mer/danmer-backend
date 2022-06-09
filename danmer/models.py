from django.db import models
from django.conf import settings

# Create your models here.


class TutorVideoPost(models.Model):
    video_title = models.CharField(max_length=100)
    video_url = models.FileField(upload_to="tutor_videos/")
    thumbnail_url = models.ImageField(upload_to="images/", null=True)
    song_artist = models.CharField(max_length=100)
    coordinate_url = models.URLField(max_length=200, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "id:" + str(self.pk) + " " + self.video_title


class TuteeVideoPost(models.Model):
    tutee_video = models.FileField(upload_to="tutee_videos/")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tutor_video = models.ForeignKey("TutorVideoPost", on_delete=models.CASCADE)
    feedback_result = models.JSONField(default=dict, null=True)  # distance result

    def __str__(self):
        return (
            "tutee_id:"
            + str(self.pk)
            + ", tutor_id:"
            + str(self.tutor_video.pk)
            + ", title:"
            + self.tutor_video.video_title
        )
