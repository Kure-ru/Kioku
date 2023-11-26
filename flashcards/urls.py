from django.urls import path
from . import views

app_name = "flashcards"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # /flashcards/:id
    path("<int:flashcard_id>/", views.DetailView.as_view(), name="detail"),
    # /flashcards/:id/answer
    path("<int:flashcard_id>/answer", views.answer, name="answer"),
    # /flashcards/logout
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
