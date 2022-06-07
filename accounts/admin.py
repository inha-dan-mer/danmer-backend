from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from django_eventstream.models import Event, EventCounter

admin.site.register(Event)
admin.site.register(EventCounter)
User = get_user_model()

admin.site.register(User)
