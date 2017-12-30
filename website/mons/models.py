"""
    This is the models module
"""
# import datetime

from django.db import models
# from django.utils import timezone

class Monster(models.Model):
    """
        This is the Monster model

        * awaken_name
        * element
        * full_name
        * get_from
        * good_for
        * grade
        * grade_num
        * image_sleepy
        * image_awake
        * link_dark
        * link_fire
        * link_light
        * link_water
        * link_wind
        * mon_type
        * rating_keep
        * rating_food
        * rating_best
        * rating_meh
        * score_total
        * score_user
        * skillup_info
        * sleepy_name
        * when_awakened
    """
    awaken_name = models.CharField(
        default='',
        max_length=50,
        unique=True,
        verbose_name='Awakened Name')
    element = models.CharField(
        choices=[
            ('Dark', 'Dark'),
            ('Fire', 'Fire'),
            ('Light', 'Light'),
            ('Water', 'Water'),
            ('Wind', 'Wind')
        ],
        default='Fire',
        max_length=50,
        verbose_name='Element')
    full_name = models.CharField(
        default='',
        max_length=200,
        unique=True,
        verbose_name='Full Name')
    get_from = models.CharField(
        default='',
        max_length=200,
        verbose_name='Get From')
    good_for = models.CharField(
        default='',
        max_length=200,
        verbose_name='Good For')
    grade = models.CharField(
        default='',
        max_length=50)
    grade_num = models.SmallIntegerField(
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        default=1,
        verbose_name='Grade Number')
    image_sleepy = models.CharField(
        default='',
        max_length=150,
        verbose_name='Sleepy Image')
    image_awake = models.CharField(
        default='',
        max_length=150,
        verbose_name='Awake Image')
    link_dark = models.CharField(
        default='',
        max_length=100,
        verbose_name='Dark Link')
    link_fire = models.CharField(
        default='',
        max_length=100,
        verbose_name='Fire Link')
    link_light = models.CharField(
        default='',
        max_length=100,
        verbose_name='Light Link')
    link_water = models.CharField(
        default='',
        max_length=100,
        verbose_name='Water Link')
    link_wind = models.CharField(
        default='',
        max_length=100,
        verbose_name='Wind Link')
    mon_type = models.CharField(
        choices=[
            ('Attack', 'Attack'),
            ('Defense', 'Defense'),
            ('HP', 'HP'),
            ('Support', 'Support')
        ],
        default='Support',
        max_length=25,
        verbose_name='Monster Type')
    rating_keep = models.FloatField(
        default=0,
        verbose_name='Rating: Keep')
    rating_food = models.FloatField(
        default=0,
        verbose_name='Rating: Food')
    rating_best = models.FloatField(
        default=0,
        verbose_name='Rating: The Best')
    rating_meh = models.FloatField(
        default=0,
        verbose_name='Rating: Meh')
    score_total = models.FloatField(
        default=0,
        verbose_name='Total Score')
    score_user = models.FloatField(
        default=0,
        verbose_name='User Score')
    skillup_info = models.CharField(
        default='',
        max_length=200,
        verbose_name='Skillup Information')
    sleepy_name = models.CharField(
        default='',
        max_length=50,
        verbose_name='Sleepy Name')
    when_awakened = models.CharField(
        default='',
        max_length=200,
        verbose_name='When Awakened')
    # pub_date = models.DateTimeField('date published')

    def __str__(self):# pragma: no cover
        """
            This method provides a useful string representation
            of this model
        """
        return f'[{self.full_name} | {self.element}]'

    # is_recent_publication.admin_order_field = 'pub_date'
    # is_recent_publication.boolean = True
    # is_recent_publication.short_description = 'Published recently?'
