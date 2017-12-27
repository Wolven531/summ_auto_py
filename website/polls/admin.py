"""
    This is the admin module

    Register models below so that they appear in the admin
"""

from django.contrib import admin
from .models import Question
from .models import Choice

admin.site.register(Question)
admin.site.register(Choice)
