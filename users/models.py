from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Profile(models.Model):
    choices = (
('Admin','Admin'),
        ('User','Faculty'),
        ('Feedbackofficer','Feedbackofficer')
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=500,blank=True,null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=50,choices=choices,default='Select your role',null=True,blank=True)
    verified = models.BooleanField(default=False,null=True,blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(null=True,blank=True,upload_to = "profiles/",default = 'profiles/user-default.png')
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)


class Emotion(models.Model):
    EMOTION_CHOICES = (
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('surprised', 'Surprised'),
        ('disgusted', 'Disgusted'),
        ('fearful', 'Fearful'),
        ('neutral', 'Neutral'),
        # Add more emotion choices as needed
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.username} - {self.emotion} - {self.timestamp}"

  
