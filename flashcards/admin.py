from django.contrib import admin

# Register your models here.
from .models import Flashcard, UserProgress

admin.site.register(Flashcard)
admin.site.register(UserProgress)