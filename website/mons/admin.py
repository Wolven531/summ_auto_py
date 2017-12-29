"""
    This is the admin module

    Register models below so that they appear in the admin
"""

from django.contrib import admin
from .models import Monster

# class ChoiceInline(admin.StackedInline):
# class ChoiceInline(admin.TabularInline):
#     """
#         This class is used to display Choice model options
#         in line in the django admin page for a Question model
#     """
#     model = Choice
#     extra = 3

class MonsterAdmin(admin.ModelAdmin):
    """
        This class is used by django admin to generate
        admin pages related to the Monster model
    """
    # date_hierarchy = 'pub_date'
    # list_display = ('question_text', 'pub_date', 'is_recent_publication')
    # list_filter = ['pub_date']
    # list_per_page = 50
    # # fields = ['question_text', 'pub_date']
    # fieldsets = [
    #     (None, {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']})
    # ]
    # inlines = [ChoiceInline]
    # search_fields = ['question_text']

admin.site.register(Monster, MonsterAdmin)
# admin.site.register(Choice)
