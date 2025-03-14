from django.db.models import F , Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
class IndexView(generic.ListView):
    template_name = "mypoll/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "mypoll/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "mypoll/results.html"
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "mypoll/detail.html", {"question": question})

def private_questions(request):
    private_question = Question.objects.filter(is_private=True).order_by("-pub_date")  
    return render(request, "mypoll/privatequestion.html", {"questions": private_question})

def private_question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id, is_private=True)
    return render(request, "mypoll/privatequestion_detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "mypoll/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "mypoll/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("mypoll:results", args=(question.id,)))




def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "mypoll/index.html", context)


def warmHot(request):
    questions = Question.objects.annotate(total_votes=Sum("choice__votes"))

    warm_questions = questions.filter(total_votes__gt=10, total_votes__lt=50)
    hot_questions = questions.filter(total_votes__gt=50)

    context = {
        "warm_questions": warm_questions,
        "hot_questions": hot_questions
    }
    return render(request, "mypoll/warmHot.html", context)