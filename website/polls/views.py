"""
    This is the views module
"""
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

TEMPLATE_DIR = 'polls'

class IndexView(generic.ListView):
    """
        This generic view is the index for the polls app
    """
    template_name = f'{TEMPLATE_DIR}/index.html'
    context_object_name = 'question_list'
    NUM_TO_RETRIEVE = 5

    def get_queryset(self):
        """
            Return the last self.NUM_TO_RETRIEVE published questions
        """
        return Question.objects.order_by('-pub_date')[:self.NUM_TO_RETRIEVE]

class DetailView(generic.DetailView):
    """
        This generic view is the detail for a specific Question
    """
    model = Question
    template_name = f'{TEMPLATE_DIR}/detail.html'

class ResultsView(generic.DetailView):
    """
        This generic view is the results for a specific Question
    """
    model = Question
    template_name = f'{TEMPLATE_DIR}/results.html'

def vote(request, question_id):
    """
        This view is for voting on a specific question
        * question_id number
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        post_val = request.POST['choice']
        selected_val = int(post_val)
        selected_choice = question.choice_set.get(pk=selected_val)
    except (KeyError, ValueError, Choice.DoesNotExist) as parse_exception:
        error_msg = 'You did not select a choice'
        if isinstance(parse_exception, ValueError):
            error_msg = f'Could not parse `post_val`=`{post_val}`'
        elif isinstance(parse_exception, Choice.DoesNotExist):
            error_msg = f'Choice did not exist `selected_val`=`{selected_val}`'
        return render(
            request,
            f'{TEMPLATE_DIR}/detail.html',
            {
                'question': question,
                'error_message': error_msg
            }
        )
    # NOTE: The line below is inspired by
    # https://docs.djangoproject.com/en/2.0/ref/models/expressions/#avoiding-race-conditions-using-f
    selected_choice.votes = F('votes') + 1
    selected_choice.save()
    # NOTE: return an HttpResponseRedirect after POST data.
    # This prevents data from posting more than once
    # return HttpResponseRedirect(reverse('polls:results', kwargs={'question_id': question.id}))
    return HttpResponseRedirect(reverse('polls:results', args=[question.id]))
