from django.db import models
from django.forms import ModelForm

# Create your models here.

class Story(models.Model):
    upload = models.TextField()

    def __str__(self):
        return self.upload

class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = ["upload"]
"""
class Literature(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=128)
    description = models.TextField(default='')
    thumbnail = models.ImageField(upload_to=thumbnail_path)
    owner = models.CharField(max_length=128)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class LiteratureForm(ModelForm):
    class Meta:
        model = Literature
        fields = "text title description thumbnail".split()
        """