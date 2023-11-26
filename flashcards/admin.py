from django.contrib import admin

# Register your models here.
from .models import User, Flashcard, UserProgress

admin.site.register(User)
admin.site.register(Flashcard)
admin.site.register(UserProgress)