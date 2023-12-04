from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db import models

class Deck(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
class Flashcard(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    deck = models.ForeignKey(Deck, on_delete=models.SET_NULL, blank=True, null=True, related_name="flashcards")
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
