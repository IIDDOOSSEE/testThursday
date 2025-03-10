from django.db.models import F
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


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "mypoll/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("mypoll:results", args=(question.id,)))




def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "mypoll/index.html", context)

# Leave the rest of the views (detail, results, vote) unchanged

def warmHot(request):
    warmQuestion = Question.objects.all()
    print(warmQuestion)
    # print(warmQuestion.question_text)
    hotQuestion = Question.objects.all()
    context = {
        "warm" : warmQuestion,
        "hot" : hotQuestion
    }
    return render(request,"mypoll/warmHot.html",context)