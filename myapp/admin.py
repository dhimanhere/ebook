from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(EbookModel)
admin.site.register(Uploader)
admin.site.register(Language)