"""
    This is the models module
"""
import datetime

from django.db import models
from django.utils import timezone

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
    awaken_name = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')

    def __str__(self):# pragma: no cover
        """
            This method provides a useful string representation
            of this model
        """
        return f'[{self.awaken_name}]'

    # is_recent_publication.admin_order_field = 'pub_date'
    # is_recent_publication.boolean = True
    # is_recent_publication.short_description = 'Published recently?'
