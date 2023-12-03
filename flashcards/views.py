from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic, View
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import BaseUserCreationForm

from .models import Flashcard

class DashboardView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:index'
    redirect_field_name = 'redirect_to'
    template_name = "flashcards/dashboard.html"

    def get(self, request):
        flashcard = Flashcard.objects.filter(next_due_date__lte=timezone.now()).order_by("?").first()
        if flashcard is None:
            return render(request, self.template_name, {"flashcard" : None})
        else:
            return render(request, self.template_name, {"flashcard" : flashcard})

class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = 'accounts:index'
    redirect_field_name = 'redirect_to'
    model = Flashcard
    template_name = "flashcards/detail.html"

    def get(self, request, flashcard_id):
        flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
        return render(request, self.template_name, {"flashcard" : flashcard})

    def post(self, request, flashcard_id):
        current_flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
        current_flashcard.last_seen = timezone.now()

        selected_answer = request.POST["answer"]
        if selected_answer == "good":
            current_flashcard.next_due_date = timezone.now() + timezone.timedelta(days=3)
        else:
            current_flashcard.next_due_date = timezone.now()
        current_flashcard.save()

        # Get the next flashcard
        next_flashcard = Flashcard.objects.filter(next_due_date__lte=timezone.now()).order_by("?").first()
        if next_flashcard is None:
            return redirect("flashcards:dashboard")
        else :
            return redirect("flashcards:detail", flashcard_id=next_flashcard.id)

class CreateView(View):
    template_name = "flashcards/new.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            question = request.POST['question']
            answer = request.POST['answer']
            user = request.user
            # tags = request.POST['tags']
            print(question, answer, user)
            flashcard = Flashcard(question=question, answer=answer, user=user)
            flashcard.save()
            return redirect("flashcards:dashboard")
        except:
            return render(request, self.template_name, {'error': 'An error occurred while creating the flashcard'})

class LoginView(View):
    def get(self, request):
        return render(request, "accounts/index.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("flashcards:dashboard")
        else :
            return render(request, "flashcards/index.html", {"error_message" : "Invalid username or password"})

class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html")

    def post(self, request):
        form = BaseUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("flashcards:dashboard")
        else:
            return render(request, 'accounts/register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("flashcards:index")