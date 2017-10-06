from django.contrib.auth.models import Permission, User
from django.db import models


class Information1(models.Model):
    user = models.ForeignKey(User, default=1)
    full_name = models.CharField(max_length=250)
    email = models.CharField(max_length=500)
    course = models.CharField(max_length=100)
    picture_topic = models.FileField()
    is_favorite = models.BooleanField(default=False)
    tutorial_date = models.DateField()
    tutorial_start = models.TimeField()
    tutorial_end = models.TimeField()

    def __str__(self):
        return self.email + ' - ' + self.full_name


class Song(models.Model):
    info = models.ForeignKey(Information1, on_delete=models.CASCADE)
    info_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.info_title


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User)
    type = models.CharField(max_length=250)
    contact_number = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.name




