from django.db import models
from django.forms import ModelForm

def user_directory_path(instance, filename):
    return '{0}/audio/{1}'.format(instance.owner, filename)

# Create your models here.
class Audio(models.Model):
    original = models.FileField(upload_to=user_directory_path)
    title = models.CharField(max_length=128)
    description = models.TextField(default='')
    owner = models.CharField(max_length=128)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class AudioForm(ModelForm):
   class Meta:
       model = Audio
       fields = "original title description".split()