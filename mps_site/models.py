from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Award(models.Model):
    id = models.AutoField(primary_key=True)
    award_description = models.CharField(max_length=100)

    def __str__(self):
        return self.award_description

class About(models.Model):
    id = models.AutoField(primary_key=True)
    about_title = models.CharField(max_length=100)
    about_description = models.TextField()
    about_ending = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.about_title

class DCUfmFamilyTree(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.year + " - " +self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    author_slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=Author)
def create_author_slug(sender, instance, **kwargs):
    if not instance.author_slug:
        instance.author_slug = slugify(instance.name)

class Post(models.Model):
    title = models.CharField(max_length=255)
    post_slug = models.SlugField(max_length=255, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    preview_image = models.CharField(max_length=255, default="assets/img/other/blank_event.png")
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        return self.title
    
@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, **kwargs):
    if not instance.post_slug:
        instance.post_slug = slugify(instance.title)

class Comment(models.Model):
    comment_author = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_on} on '{self.post}'"