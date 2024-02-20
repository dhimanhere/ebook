from django.db import models
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

# Create your models here.
class Institute(models.Model):
	name = models.CharField(max_length = 50)
	slug = AutoSlugField(populate_from='title', unique=True)
	about = models.TextField()
	created_on=models.DateTimeField(auto_now_add=True)

class EbookModel(models.Model):
	title = models.CharField(max_length = 255)
	slug = AutoSlugField(populate_from='title', unique=True)
	thumbnail = models.ImageField(upload_to = "thumbnail/", null=True)
	description = RichTextField()
	book = models.FielField(upload_to="ebook/", null=True)
	author = models.CharField(max_length=30)
	created_on = models.DateTimeField(auto_now_add = True)