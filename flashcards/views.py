from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import BaseUserCreationForm

from .models import Flashcard, Deck

class DashboardView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:index'
    redirect_field_name = 'redirect_to'
    template_name = "flashcards/dashboard.html"
    model = Deck

    def get(self, request):
        decks = Deck.objects.all()
        return render(request, self.template_name, {"decks" : decks})

    def post(self, request):
        try:
            deck_name = request.POST['deck_name']
            new_deck = Deck(user=request.user, name=deck_name)
            new_deck.save()
            messages.success(request, 'Deck created successfully.')
            return redirect('flashcards:dashboard')
        except ValueError:
            messages.error(request, 'There was an error. Please try again')
            return redirect('flashcards:dashboard')
class DeckView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:index'
    redirect_field_name = 'redirect_to'
    template_name = "flashcards/deck.html"
    model = Deck

    def get(self, request, deck_id):
        deck = get_object_or_404(self.model, pk=deck_id)
        flashcard = Flashcard.objects.filter(next_due_date__lte=timezone.now(), deck=deck).order_by("?").first()
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
        current_flashcard = get_object_or_404(self.model, pk=flashcard_id)
        current_flashcard.last_seen = timezone.now()

        selected_answer = request.POST["answer"]
        if selected_answer == "good":
            current_flashcard.next_due_date = timezone.now() + timezone.timedelta(days=3)
        else:
            current_flashcard.next_due_date = timezone.now()
        current_flashcard.save()

        # Get the next flashcard
        deck = current_flashcard.deck
        next_flashcard = self.model.objects.filter(next_due_date__lte=timezone.now(), deck=deck).order_by("?").first()
        if next_flashcard is None:
            return redirect("flashcards:dashboard")
        else :
            return redirect('flashcards:detail', flashcard_id=next_flashcard.id)

class CreateView(View):
    template_name = "flashcards/new.html"
    flashcard_model = Flashcard
    deck_model = Deck

    def get(self, request):
        user_decks = Deck.objects.filter(user=request.user)
        return render(request, self.template_name, {'decks': user_decks})

    def post(self, request):
        try:
            question = request.POST['question']
            answer = request.POST['answer']
            deck_id = request.POST['deck']

            deck = get_object_or_404(Deck, pk=deck_id)

            flashcard = Flashcard(question=question, answer=answer, user=request.user, deck=deck)
            flashcard.save()
            messages.success(request, 'Flashcard created successfully.')

            user_decks = Deck.objects.filter(user=request.user)
            return render(request, self.template_name, {'decks': user_decks})
        except:
            messages.error(request, "An error occurred while creating the flashcard" )
            return render(request, self.template_name, {'error': 'An error occurred while creating the flashcard'})

class EditView(View):
    template_name = "flashcards/edit.html"
    flashcard_model = Flashcard
    deck_model = Deck

    def get(self, request):
        flashcards = self.flashcard_model.objects.filter(user=request.user)
        return render(request, self.template_name, {'flashcards': flashcards})

    def post(self, request):
            flashcard_id = request.POST['id']
            print(flashcard_id)
            try:
                flashcard = self.flashcard_model.objects.get(id=flashcard_id)
            except self.flashcard_model.DoesNotExist:
                return render(request, self.template_name, {'error': 'Flashcard does not exist'})

            flashcard.question = request.POST['question']
            flashcard.answer = request.POST['answer']
            deck_id = request.POST['deck']
            deckObj = get_object_or_404(Deck, pk=deck_id)
            flashcard.deck = deckObj
            flashcard.save()
            return redirect("flashcards:dashboard")

class DeleteView(View):
    def post(self, request, flashcard_id):
        flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
        flashcard.delete()
        return redirect('flashcards:dashboard')

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