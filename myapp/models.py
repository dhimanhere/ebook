from django.db import models
from autoslug import AutoSlugField
from django_quill.fields import QuillField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 50)
	image = models.ImageField(upload_to='category/')
	slug = AutoSlugField(populate_from='name', unique=True)
	created_on=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Uploader(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 50)
	image = models.ImageField(upload_to = 'author', null = True, blank = True)
	url = models.URLField(max_length = 600, null = True, blank = True)
	slug = AutoSlugField(populate_from='name', unique=True)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Language(models.Model):
	name = models.CharField(max_length = 20)
	slug = AutoSlugField(populate_from="name", unique = True)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class EbookModel(models.Model):
	title = models.CharField(max_length = 255)
	slug = AutoSlugField(populate_from='title', unique=True)
	thumbnail = models.ImageField(upload_to = "thumbnail/", null=True)
	description = QuillField()
	book = models.FileField(upload_to="ebook/", null=True)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	uploader = models.ForeignKey(Uploader, on_delete = models.CASCADE)
	author = models.CharField(max_length=30)
	store = models.URLField(max_length = 200, blank = True, null = True)
	language = models.ForeignKey(Language, on_delete = models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.title