from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Room(models.Model):
    name = models.CharField(max_length=1000,unique=True)
    users = models.ManyToManyField(User, related_name='rooms')
    code = models.CharField(max_length=50, default='',unique=True)
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    create_date = models.DateTimeField()
    def __str__(self):
        return self.name
    
class Notice(models.Model):
    title = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author_notice')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title