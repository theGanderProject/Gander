from django.db import models
from django.forms import ModelForm
from tempfile import TemporaryFile
from PIL import Image as PILImage
from django.core.files.base import File
from os.path import splitext
from django.contrib.auth.models import User
import hashlib

def md5sum(f):
    d = hashlib.md5()
    for chunk in f.chunks():
        d.update(chunk)
    return d.hexdigest()

def create_thumbnail_file(f, dimensions=(128, 128)):
    image = PILImage.open(f)
    if image.mode == "RGBA":
        alpha = image.split()[3]
        extrema = alpha.getextrema()
        if extrema != (255,255): # if uses alpha channels
            image_with_background = PILImage.new('RGB', image.size, (245, 245, 241))
            image_with_background.paste(image, mask=alpha) # TODO: Explain this line
            image = image_with_background

    image.thumbnail(dimensions)
    tempfile = TemporaryFile()
    image.convert('RGB').save(tempfile, 'JPEG')

    thumbnail_file = File(tempfile)
    thumbnail_file.name = splitext(f.name)[0] + '.jpeg'

    return thumbnail_file

def original_path(instance, filename):
    return '{0}/art/{1}'.format(instance.owner, filename)

def thumbnail_path(instance, filename):
    return '{0}/art/thumbnail_{1}'.format(instance.owner, filename)

def user_small_path(instance, filename):
    return '{0}/art/small_{1}'.format(instance.owner, filename)

def user_medium_path(instance, filename):
    return '{0}/art/medium_{1}'.format(instance.owner, filename)

def user_large_path(instance, filename):
    return '{0}/art/large_{1}'.format(instance.owner, filename)

def user_huge_path(instance, filename):
    return '{0}/art/huge_{1}'.format(instance.owner, filename)


# Create your models here.

class Tag(models.Model):
    text = models.CharField(max_length=32, unique=True)

class Image(models.Model):
    original = models.ImageField(upload_to=original_path)
    title = models.CharField(max_length=128, blank=True)
    description = models.TextField(default='', blank=True)
    owner = models.ForeignKey(User, related_name="image_owner")
    md5 = models.CharField(max_length=32)
    favorite = models.ManyToManyField(User, related_name="image_favorite")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to=thumbnail_path)
    small = models.ImageField(upload_to=user_small_path, null=True)
    medium = models.ImageField(upload_to=user_medium_path, null=True)
    large = models.ImageField(upload_to=user_large_path, null=True)
    huge = models.ImageField(upload_to=user_huge_path, null=True)
    tag = models.ManyToManyField(Tag, related_name="tag")

    def save(self, *args, **kwargs):
        if self.pk is None:
            new_image = True
        else:
            entry_to_replace = Image.objects.get(pk=self.pk)
            new_image = entry_to_replace.original != self.original
        if new_image:
            self.md5 = md5sum(self.original)
            self.thumbnail = create_thumbnail_file(self.original)
            if (self.original.width > 256 or self.original.height > 256):
                self.small = create_thumbnail_file(self.original, (256,256))
            if (self.original.width > 512 or self.original.height > 512):
                self.medium = create_thumbnail_file(self.original, (512,512))
            if (self.original.width > 1024 or self.original.height > 1024):
                self.large = create_thumbnail_file(self.original, (1024,1024))
            if (self.original.width > 2048 or self.original.height > 2048):
                self.huge = create_thumbnail_file(self.original, (2048,2048))
        super(Image, self).save(*args, **kwargs)

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = "original".split()