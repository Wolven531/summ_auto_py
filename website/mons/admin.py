"""
	This is the admin module

	Register models below so that they appear in the admin
"""

from django.contrib import admin
from .models import Monster

# class ChoiceInline(admin.StackedInline):
# class ChoiceInline(admin.TabularInline):
#	 """
#		 This class is used to display Choice model options
#		 in line in the django admin page for a Question model
#	 """
#	 model = Choice
#	 extra = 3

class MonsterAdmin(admin.ModelAdmin):
	"""
		This class is used by django admin to generate
		admin pages related to the Monster model
	"""
	# date_hierarchy = 'pub_date'
	list_display = (
		'awaken_name',
		'element',
		'sleepy_name',
		'grade_num',
		'score_total',
		'score_user',
		'rating_keep',
		'rating_food',
		'rating_best',
		'rating_meh')
	list_filter = ['element', 'mon_type', 'grade_num', 'good_for']
	list_per_page = 50
	# # fields = ['question_text', 'pub_date']
	fieldsets = [
		(
			'Name Information',
			{
				'fields': ['full_name', 'sleepy_name', 'awaken_name'],
				'classes': []
			}
		),
		(
			'Miscellaneous Information',
			{
				'fields': [
					'element',
					'get_from',
					'good_for',
					'mon_type',
					'skillup_info',
					'when_awakened'
				]
			}
		),
		('Grade Information', {'fields': ['grade', 'grade_num'], 'classes': ['collapse']}),
		('Image Information', {'fields': ['image_sleepy', 'image_awake'], 'classes': ['collapse']}),
		(
			'Link Information',
			{
				'fields': ['link_dark', 'link_fire', 'link_light', 'link_water', 'link_wind'],
				'classes': ['collapse']
			}
		),
		(
			'Rating Information',
			{
				'fields': ['rating_keep', 'rating_food', 'rating_best', 'rating_meh'],
				'classes': ['collapse']
			}
		),
		('Score Information', {'fields': ['score_total', 'score_user'], 'classes': ['collapse']})
	]
	# inlines = [ChoiceInline]
	search_fields = ['sleepy_name', 'awaken_name', 'element', 'mon_type', 'good_for']

admin.site.register(Monster, MonsterAdmin)
# admin.site.register(Choice)
