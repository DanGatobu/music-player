from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class audio(models.Model):
    name=models.CharField(max_length=600)
    album=models.CharField(max_length=500)
    artist=models.CharField(max_length=500)
    length=models.DurationField() 
    link=models.FileField(upload_to='music/',max_length=600)
    favorite_bool=models.BooleanField(default=False,null=False)
    def __str__(self):
        return self.name
    
class favorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    song=models.ForeignKey(audio,on_delete=models.CASCADE)
    
class playlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField(max_length=100)
    song=models.ManyToManyField(audio)
    
class test(models.Model):
    songlink=models.CharField(max_length=600)
    
    