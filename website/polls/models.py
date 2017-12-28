"""
    This is the models module
"""
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """
        This is the Question model

        * question_text
        * pub_date
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
            This method provides a useful string representation
            of this model
        """
        return f'Question[{self.question_text}, {self.pub_date}]'

    def is_recent_publication(self):
        """
            Returns True if this question was published
            within the past day; False otherwise
        """
        now = timezone.now()
        earliest_recent = now - datetime.timedelta(days=1)
        if now < self.pub_date:
            return False
        return self.pub_date >= earliest_recent


class Choice(models.Model):
    """
        This is the Choice model

        * question
        * choice_text
        * votes
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
            This method provides a useful string representation
            of this model
        """
        return f'Choice[{self.choice_text}, {self.votes}]'
