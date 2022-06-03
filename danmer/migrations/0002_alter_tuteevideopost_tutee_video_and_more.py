# Generated by Django 4.0.3 on 2022-06-03 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('danmer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuteevideopost',
            name='tutee_video',
            field=models.FileField(upload_to='tutee_videos/'),
        ),
        migrations.AlterField(
            model_name='tutorvideopost',
            name='thumbnail_img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='tutorvideopost',
            name='video',
            field=models.FileField(upload_to='tutor_videos/'),
        ),
    ]
