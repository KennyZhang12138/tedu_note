from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField('Username', max_length=30, unique=True)
    password = models.CharField('Password', max_length=32)
    create_time = models.DateTimeField('Create Time', auto_now_add=True)
    update_time = models.DateTimeField('Update Time', auto_now=True)

    def __str__(self):
        return "User " + self.username

