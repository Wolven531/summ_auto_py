"""
    This is the views module
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

def index(request):
    """
        This view is the index for the polls app
    """
    num_to_retrieve = 5
    question_list = Question.objects.order_by('-pub_date')[:num_to_retrieve]
    context = {'question_list': question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    """
        This view is for viewing the details of a specific question
        * question_id number
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    """
        This view is for viewing the results of a specific question
        * question_id number
    """
    return HttpResponse(f'You are viewing the results of question {question_id}')

def vote(request, question_id):
    """
        This view is for voting on a specific question
        * question_id number
    """
    return HttpResponse(f'You are voting on question {question_id}')
