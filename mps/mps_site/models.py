from django.db import models

# Create your models here.

class AboutUs(models.Model):
    heading = models.CharField(max_length=100)
    sub_heading = models.CharField(max_length=100)
    text_1 = models.TextField()
    text_2 = models.TextField()
    signature = models.CharField(max_length=100)

class ReasonsToJoin(models.Model):
    heading = models.CharField(max_length=100)
    sub_heading = models.CharField(max_length=100)
    reason_1 = models.TextField()
    reason_2 = models.TextField()
    reason_3 = models.TextField()
    reason_4 = models.TextField()

class Award(models.Model):
    award_description = models.CharField(max_length=100)

class AwardsHistory(models.Model):
    heading = models.CharField(max_length=100)
    awards = models.ForeignKey(Award, on_delete=models.CASCADE)

class CommitteeMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    social_link_1 = models.CharField(max_length=100)
    social_link_2 = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to='committee_members/')

class Commitee(models.Model):
    id = models.AutoField(primary_key=True)
    committee_member = models.ForeignKey(CommitteeMember, on_delete=models.CASCADE)