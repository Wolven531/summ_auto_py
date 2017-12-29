"""
    This is the views module
"""
# from django.db.models import F
# from django.http import HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.utils import timezone
from django.views import generic
from .models import Monster

TEMPLATE_DIR = 'mons'

class IndexView(generic.ListView):# pylint: disable=R0901
    """
        This generic view is the index for the mons app
    """
    template_name = f'{TEMPLATE_DIR}/index.html'
    context_object_name = 'monster_list'

    def get_queryset(self):
        """
            Return all mons ordered by their awakened name
        """
        return Monster.objects.all().order_by('awaken_name')

class DetailView(generic.DetailView):# pylint: disable=R0901
    """
        This generic view is the detail for a specific Monster
    """
    model = Monster
    template_name = f'{TEMPLATE_DIR}/detail.html'
