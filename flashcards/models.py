from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

class Flashcard(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
   # tags = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    next_due_date = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return self.question

    def is_due(self):
        return self.next_due_date <= timezone.now()

class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name="user_progress")

    def __str__(self) -> str:
        return self.progress_status
