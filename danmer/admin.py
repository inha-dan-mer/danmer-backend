from django.contrib import admin
from .models import TutorVideoPost, TuteeVideoPost, Feedback
# Register your models here.
admin.site.register(TutorVideoPost)
admin.site.register(TuteeVideoPost)
admin.site.register(Feedback)