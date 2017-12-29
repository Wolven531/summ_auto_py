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
        * links
        * mon_type
        * ratings
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
        default='',
        max_length=50)
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
    # TODO: links
    mon_type = models.CharField(
        default='',
        max_length=25,
        verbose_name='Monster Type')
    # TODO: ratings
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
        unique=True,
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
