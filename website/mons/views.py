"""
	This is the views module
"""
import json
import os
# from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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

def load_from_disk(filepath):
	"""
		This method attempts to load a JSON file from
		the disk, given a `filepath`
		* filepath
	"""
	data = {}
	with open(filepath, 'r') as in_file:
		data = json.load(in_file)
	return data

def create_monster(json_data):
	"""
		Create a monster with the given JSON
		* json
	"""
	# print(f'create_monster got this JSON={json_data}')
	return Monster.objects.create(
		awaken_name=json_data['name_awaken'],
		element=json_data['element'].capitalize(),
		full_name=json_data['name_full'],
		get_from=json_data['get_from'],
		good_for=json_data['good_for'],
		grade=json_data['grade'],
		grade_num=json_data['grade_num'],
		image_sleepy=json_data['links']['IMAGE_SLEEPY'],
		image_awake=json_data['links']['IMAGE_AWAKE'],
		link_dark=json_data['links']['DARK'],
		link_fire=json_data['links']['FIRE'],
		link_light=json_data['links']['LIGHT'],
		link_water=json_data['links']['WATER'],
		link_wind=json_data['links']['WIND'],
		mon_type=json_data['mon_type'],
		rating_keep=json_data['ratings']['KEEP_IT'],
		rating_food=json_data['ratings']['FOOD'],
		rating_best=json_data['ratings']['THE_BEST'],
		rating_meh=json_data['ratings']['MEH'],
		score_total=json_data['score_total'],
		score_user=json_data['score_user'],
		skillup_info=json_data['skillup_info'],
		sleepy_name=json_data['name_sleepy'],
		when_awakened=json_data['when_awaken'])

def load_monsters(request):
	"""
		This view is for providing control via the website
		to load monsters from the parsed JSON files
	"""
	if request.method.lower() == 'get':
		return render(request, template_name=f'{TEMPLATE_DIR}/load.html', status=200)

	curr_dir = os.path.dirname(os.path.abspath(__file__))
	website_dir = os.path.dirname(curr_dir)
	summ_auto_repo_dir = os.path.dirname(website_dir)
	mon_data_dir = os.path.join(summ_auto_repo_dir, 'data', 'mons')

	for filepath in os.listdir(mon_data_dir):
		full_path = os.path.join(mon_data_dir, filepath)
		json_mon = load_from_disk(full_path)
		awaken_name = json_mon['name_awaken']
		# print(f'Looking up with awaken_name={awaken_name}')

		try:
			# NOTE: we use awaken name because it is unique
			old_mon = Monster.objects.get(awaken_name=awaken_name)
			# print(f'Monster is old={filepath}')

			old_mon.awaken_name = json_mon['name_awaken']
			old_mon.element = json_mon['element'].capitalize()
			old_mon.full_name = json_mon['name_full']
			old_mon.get_from = json_mon['get_from']
			old_mon.good_for = json_mon['good_for']
			old_mon.grade = json_mon['grade']
			old_mon.grade_num = json_mon['grade_num']
			old_mon.image_sleepy = json_mon['links']['IMAGE_SLEEPY']
			old_mon.image_awake = json_mon['links']['IMAGE_AWAKE']
			old_mon.link_dark = json_mon['links']['DARK']
			old_mon.link_fire = json_mon['links']['FIRE']
			old_mon.link_light = json_mon['links']['LIGHT']
			old_mon.link_water = json_mon['links']['WATER']
			old_mon.link_wind = json_mon['links']['WIND']
			old_mon.mon_type = json_mon['mon_type']
			old_mon.rating_keep = json_mon['ratings']['KEEP_IT']
			old_mon.rating_food = json_mon['ratings']['FOOD']
			old_mon.rating_best = json_mon['ratings']['THE_BEST']
			old_mon.rating_meh = json_mon['ratings']['MEH']
			old_mon.score_total = json_mon['score_total']
			old_mon.score_user = json_mon['score_user']
			old_mon.skillup_info = json_mon['skillup_info']
			old_mon.sleepy_name = json_mon['name_sleepy']
			old_mon.when_awakened = json_mon['when_awaken']
		except Monster.DoesNotExist:
			# print(f'Monster is new={filepath}')
			old_mon = create_monster(json_mon)
		# print(f'Attempting to save {awaken_name} with {vars(old_mon)}')
		old_mon.save()

	return HttpResponseRedirect(reverse('mons:index'))
