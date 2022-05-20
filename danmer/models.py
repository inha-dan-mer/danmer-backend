from django.db import models
from django.conf import settings
# Create your models here.

class TutorVideoPost(models.Model): # tutor가 올리는 video post. main page에 list로 표시
    video_name = models.CharField(max_length=100)
    video = models.FileField()
    thumbnail_img = models.ImageField(upload_to = 'images/%Y/%m', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    singer = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.video_name

class TuteeVideoPost(models.Model): #tutee가 올리는 video posst
    tutee_video = models.FileField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tutor_video = models.ForeignKey("TutorVideoPost", on_delete=models.CASCADE)

class Feedback(models.Model):
    result_per_part = models.JSONField(default=dict) # body part별 정확도 모음
    post = models.ForeignKey("TuteeVideoPost", on_delete=models.CASCADE)