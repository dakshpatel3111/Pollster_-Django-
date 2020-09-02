from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Questions,Choice
from django.urls import reverse
import http


def index(request):

    latest_question_list = Questions.objects.order_by('-pub_date')[:5]
    context ={'lqt': latest_question_list}
    return render(request,'polls/index.html',context)


def details(request , question_id):
    try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'polls/details.html',{'question': question})


def results(request, question_id):
  question = get_object_or_404(Questions, pk=question_id)
  return render(request, 'polls/results.html', { 'question': question })


def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))