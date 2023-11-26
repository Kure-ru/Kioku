from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic, View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Flashcard

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'accounts:index'
    redirect_field_name = 'redirect_to'
    template_name = "flashcards/index.html"

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

def answer(request, flashcard_id):
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
            return redirect("flashcards:index")
        else :
            return redirect("flashcards:detail", flashcard_id=next_flashcard.id)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts:index")
