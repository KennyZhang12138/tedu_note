from pyexpat import model
from django.db import models
from user.models import User

# Create your models here.
class Note(models.Model):
    title = models.CharField('Title', max_length=100)
    content = models.TextField('Content')
    created_time = models.DateTimeField('create_time', auto_now_add=True)
    updated_time = models.DateTimeField('update_time', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    