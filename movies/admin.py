from django.contrib import admin

from .models import Collection, Movie

# Register your models here.

admin.site.register((Collection, Movie))
