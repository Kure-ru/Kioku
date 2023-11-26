from django.contrib import admin
# The include() function allows referencing other URLconfs.
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("flashcards/", include("flashcards.urls")),
    path('', include('accounts.urls')),
]
