import datetime

from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.username

class Flashcard(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flashcards")
    tags = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    next_due_date = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.question
    
    def is_due(self):
        return self.next_due_date <= timezone.now()

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_progress")
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name="user_progress")

    def __str__(self) -> str:
        return self.progress_status
