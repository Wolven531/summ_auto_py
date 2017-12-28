"""
    This is the tests module for the polls application
"""

import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question

class QuestionIndexViewTests(TestCase):
    """
        This class tests the functionality of the Question index view
    """

    @classmethod
    def create_question(cls, question_text, days_offset):
        """
            Create a question with the given `question_text` and published the
            given number of `days` offset to now (negative for questions published
            in the past, positive for questions that have yet to be published)
        """
        published = timezone.now() + datetime.timedelta(days=days_offset)
        return Question.objects.create(question_text=question_text, pub_date=published)

    def test_index_should_be_empty_when_no_questions(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there are no questions to display
        """
        # setup
        # execute
        response = self.client.get(reverse('polls:index'))

        # verify
        self.assertContains(response, 'No polls are available', status_code=200)
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_index_should_be_empty_when_only_future_questions(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there are only future questions to display (i.e. it
            does not display the future questions)
        """
        # setup
        self.create_question('Future question', 30)

        # execute
        response = self.client.get(reverse('polls:index'))

        # verify
        self.assertContains(response, 'No polls are available', status_code=200)
        self.assertQuerysetEqual(response.context['question_list'], [])

    def test_index_should_display_when_one_question(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there is a question from the past
        """
        # setup
        past_question = self.create_question('Past question', -30)

        # execute
        response = self.client.get(reverse('polls:index'))

        # verify
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            list(response.context['question_list']),
            [past_question])

    def test_index_should_display_ordered_when_multiple_questions(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there is more than one question from the past (and
            that they are in order)
        """
        # setup
        question_past = self.create_question('Past question', -30)
        question_recent = self.create_question('Recent question', -1)

        # execute
        response = self.client.get(reverse('polls:index'))

        # verify
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            list(response.context['question_list']),
            [question_recent, question_past])

class QuestionModelTests(TestCase):
    """
        This class tests the functionality of the Question model
    """

    def test_is_recent_publication_should_return_false_when_pub_date_is_in_future(self):# pylint: disable=C0103
        """
            This test ensures that the is_recent_publication() method
            returns False when the pub_date is in the future
        """
        # setup
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        # execute
        is_recent = future_question.is_recent_publication()

        # verify
        self.assertFalse(is_recent, 'Expected question from future to not be recent')

    def test_is_recent_publication_should_return_false_when_pub_date_is_too_old(self):# pylint: disable=C0103
        """
            This test ensures that the is_recent_publication() method
            returns False when the pub_date is too old
        """
        # setup
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)

        # execute
        is_recent = old_question.is_recent_publication()

        # verify
        self.assertFalse(is_recent, 'Expected question from past to not be recent')

    def test_is_recent_publication_should_return_true_when_pub_date_is_recent(self):# pylint: disable=C0103
        """
            This test ensures that the is_recent_publication() method
            returns True when the pub_date is recent
        """
        # setup
        time = timezone.now() - datetime.timedelta(seconds=60*60*8)
        recent_question = Question(pub_date=time)

        # execute
        is_recent = recent_question.is_recent_publication()

        # verify
        self.assertTrue(is_recent, 'Expected recent question to be recent')
