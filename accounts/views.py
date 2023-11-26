from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, "accounts/index.html")
    
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("flashcards:index")
        else :
            return render(request, "accounts/index.html", {"error_message" : "Invalid username or password"})