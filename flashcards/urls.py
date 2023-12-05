from django.urls import path
from . import views


app_name = "flashcards"
urlpatterns = [
    path("", views.LoginView.as_view(), name="index"),
    path("login", views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    # /flashcards/edit
    path("edit", views.EditView.as_view(), name="edit"),
    # /flashcards/deck/:id
    path("deck/<int:deck_id>/", views.DeckView.as_view(), name="deck"),
    # /flashcards/:id
    path("<int:flashcard_id>/", views.DetailView.as_view(), name="detail"),
    # /flashcards/:id/answer
    path("<int:flashcard_id>/answer", views.DetailView.as_view(), name="post"),
    # /flashcards/new
    path('new', views.CreateView.as_view(), name="create"),
    # /flashcards/delete
    path('delete/<int:flashcard_id>/', views.DeleteView.as_view(), name='delete'),
    # /flashcards/logout
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
