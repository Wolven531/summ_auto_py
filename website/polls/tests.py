"""
    This is the tests module for the polls application
"""

import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase):
    """
        This class tests the functionality of the Question model
    """

    def test_is_recent_publication_should_return_false_when_pub_date_is_in_future(self):# pylint: disable=C0103
        """
            This test ensures that the is_recent_publication() method
            returns False when the pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(
            future_question.is_recent_publication(),
            'Expected question from future to not be recent')

    def test_is_recent_publication_should_return_false_when_pub_date_is_too_old(self):# pylint: disable=C0103
        """
            This test ensures that the is_recent_publication() method
            returns False when the pub_date is too old
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertFalse(
            old_question.is_recent_publication(),
            'Expected question from past to not be recent')

    def test_is_recent_publication_should_return_true_when_pub_date_is_recent(self):# pylint: disable=C0103
        """
            This test ensures that the is_recent_publication() method
            returns True when the pub_date is recent
        """
        time = timezone.now() - datetime.timedelta(seconds=60*60*8)
        recent_question = Question(pub_date=time)
        self.assertTrue(
            recent_question.is_recent_publication(),
            'Expected recent question to be recent')
