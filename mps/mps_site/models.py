from django.db import models

# Create your models here.

class Award(models.Model):
    id = models.AutoField(primary_key=True)
    award_description = models.CharField(max_length=100)

class About(models.Model):
    id = models.AutoField(primary_key=True)
    about_title = models.CharField(max_length=100)
    about_description = models.TextField()
    about_ending = models.CharField(max_length=100, default="")