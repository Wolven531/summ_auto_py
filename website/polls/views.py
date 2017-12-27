"""
    This is the views module
"""
# from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """
        This is the index for the polls app
    """
    return HttpResponse('Hello, world. You are at the polls index')
