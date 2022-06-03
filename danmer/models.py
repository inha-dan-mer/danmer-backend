from django.db import models
from django.conf import settings
# Create your models here.

class TutorVideoPost(models.Model): 
    video_name = models.CharField(max_length=100)
    video = models.FileField(upload_to = 'tutor_videos/')
    thumbnail_img = models.ImageField(upload_to = 'images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    singer = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.video_name

class TuteeVideoPost(models.Model): 
    tutee_video = models.FileField(upload_to = 'tutee_videos/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tutor_video = models.ForeignKey("TutorVideoPost", on_delete=models.CASCADE)

class Feedback(models.Model):
    result_per_part = models.JSONField(default=dict) 
    # FIXME
    #post = models.ForeignKey("TuteeVideoPost", on_delete=models.CASCADE)
    tutee_video_id = models.IntegerField()


