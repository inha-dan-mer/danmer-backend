# Generated by Django 4.0.3 on 2022-05-08 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('danmer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorvideopost',
            name='video_url',
        ),
        migrations.AddField(
            model_name='tutorvideopost',
            name='video',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='tuteevideopost',
            name='tutee_video_url',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]