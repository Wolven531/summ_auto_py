"""
	This is the tests module for the polls application
"""

import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question

class TestUtil():# pylint: disable=R0903
	"""
		This method houses utility methods for the tests below
	"""

	@staticmethod
	def create_question(question_text, days_offset):
		"""
			Create a question with the given `question_text` and published the
			given number of `days` offset to now (negative for questions published
			in the past, positive for questions that have yet to be published)
		"""
		published = timezone.now() + datetime.timedelta(days=days_offset)
		return Question.objects.create(question_text=question_text, pub_date=published)

	@staticmethod
	def create_choice(question_ref, display, num_votes):
		"""
			Create a choice with the given `question`, `choice_text`, and `votes`
		"""
		return Choice.objects.create(question=question_ref, choice_text=display, votes=num_votes)

class QuestionVoteViewTests(TestCase):
	"""
		This class tests the functionality of the Questions vote view
	"""

	def test_vote_should_show_error_when_no_selection(self):# pylint: disable=C0103
		"""
			This test ensures an error message is provided when
			no vote selection is made
		"""
		# setup
		past_question = TestUtil.create_question('Past question', -30)
		url = reverse('polls:vote', args=[past_question.id])

		# execute
		response = self.client.post(url)

		# verify
		self.assertContains(response, 'You did not select a choice', status_code=200)

	def test_vote_should_show_error_when_bad_choice_value_provided(self):# pylint: disable=C0103
		"""
			This test ensures an error message is provided when
			a bad value was provided for the choice
		"""
		# setup
		past_question = TestUtil.create_question('Past question', -30)
		choice1 = TestUtil.create_choice(past_question, 'Choice 1', 0)
		self.assertEqual(choice1.id, 1)
		url = reverse('polls:vote', args=[past_question.id])

		# execute
		response = self.client.post(path=url, data={'choice': 'asdf'})

		# verify
		self.assertContains(response, 'Could not parse `post_val`', status_code=200)

	def test_vote_should_show_error_when_missing_choice_value_provided(self):# pylint: disable=C0103
		"""
			This test ensures an error message is provided when
			a valid value was provided for the choice, but the value
			did not match any choices during the lookup
		"""
		# setup
		past_question = TestUtil.create_question('Past question', -30)
		choice1 = TestUtil.create_choice(past_question, 'Choice 1', 0)
		self.assertEqual(choice1.id, 1)
		url = reverse('polls:vote', args=[past_question.id])

		# execute
		response = self.client.post(path=url, data={'choice': 2})

		# verify
		self.assertContains(response, 'Choice did not exist `selected_val`', status_code=200)

	def test_vote_should_display_when_successful(self):# pylint: disable=C0103
		"""
			This test ensures that when a vote is successful, the user is
			taken to the results page and it displays properly (with the
			updated vote total)
		"""
		# setup
		past_question = TestUtil.create_question('Past question', -30)
		choice1 = TestUtil.create_choice(past_question, 'Choice 1', 0)
		self.assertEqual(choice1.id, 1)
		url = reverse('polls:vote', args=[past_question.id])
		expected_url = reverse('polls:results', args=[past_question.id])

		# execute
		response = self.client.post(path=url, data={'choice': 1})

		# verify
		updated_choice = Choice.objects.get(pk=choice1.id)
		self.assertRedirects(
			response=response,
			expected_url=expected_url,
			status_code=302,
			target_status_code=200)
		self.assertEqual(
			updated_choice.votes,
			1,
			'Expected vote view to increase vote count on choice')

class QuestionResultsViewTests(TestCase):
	"""
		This class tests the functionality of the Question results view
	"""

	def test_results_should_be_empty_when_future_question(self):# pylint: disable=C0103
		"""
			This test ensures the results view will return a 404
			when a user attempts to view the results page for a question
			that has a pub_date in the future
		"""
		# setup
		future_question = TestUtil.create_question('Future question', 30)
		url = reverse('polls:results', args=[future_question.id])

		# execute
		response = self.client.get(url)

		# verify
		self.assertEqual(
			response.status_code,
			404,
			'Expected future question results view to return 404')

	def test_results_should_display_when_past_question(self):# pylint: disable=C0103
		"""
			This test ensures the results view will display
			when a user attempts to view the results page for a question
			that has a pub_date in the past
		"""
		# setup
		past_question = TestUtil.create_question('Past question', -30)
		choice1 = TestUtil.create_choice(past_question, 'Choice 1', 0)
		choice2 = TestUtil.create_choice(past_question, 'Choice 2', 10)
		choice3 = TestUtil.create_choice(past_question, 'Choice 3', 100)
		url = reverse('polls:results', args=[past_question.id])

		# execute
		response = self.client.get(url)

		# verify
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['question'], past_question)
		self.assertListEqual(
			list(response.context['question'].choice_set.all()),
			[choice1, choice2, choice3]
		)

class QuestionDetailViewTests(TestCase):
	"""
		This class tests the functionality of the Question detail view
	"""

	def test_detail_should_be_empty_when_future_question(self):# pylint: disable=C0103
		"""
			This test ensures the detail view will return a 404
			when a user attempts to view the detail page for a question
			that has a pub_date in the future
		"""
		# setup
		future_question = TestUtil.create_question('Future question', 30)
		url = reverse('polls:detail', args=[future_question.id])

		# execute
		response = self.client.get(url)

		# verify
		self.assertEqual(
			response.status_code,
			404,
			'Expected future question detail view to return 404')

	def test_detail_should_display_when_past_question(self):# pylint: disable=C0103
		"""
			This test ensures the detail view will display
			when a user attempts to view the detail page for a question
			that has a pub_date in the past
		"""
		# setup
		past_question = TestUtil.create_question('Past question', -30)
		url = reverse('polls:detail', args=[past_question.id])

		# execute
		response = self.client.get(url)

		# verify
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['question'], past_question)

class QuestionIndexViewTests(TestCase):
	"""
		This class tests the functionality of the Question index view
	"""

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
		TestUtil.create_question('Future question', 30)

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
		past_question = TestUtil.create_question('Past question', -30)

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
		question_past = TestUtil.create_question('Past question', -30)
		question_recent = TestUtil.create_question('Recent question', -1)

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
		future_question = TestUtil.create_question('Past question', 30)

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
		old_question = TestUtil.create_question('Past question', -30)

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

class ChoiceModelTests(TestCase):
	"""
		This class tests the functionality of the Choice model
	"""

	def test_has_votes_should_return_false_when_no_votes(self):# pylint: disable=C0103
		"""
			This test ensures that the has_votes() method
			returns False when the choice has no votes
		"""
		# setup
		future_question = TestUtil.create_question('Future question', 30)
		choice = TestUtil.create_choice(future_question, 'Choice 1', 0)

		# execute
		has_votes = choice.has_votes()

		# verify
		self.assertFalse(has_votes, 'Expected choice to not have votes')

	def test_has_votes_should_return_true_when_some_votes(self):# pylint: disable=C0103
		"""
			This test ensures that the has_votes() method
			returns True when the choice has some votes
		"""
		# setup
		future_question = TestUtil.create_question('Future question', 30)
		choice = TestUtil.create_choice(future_question, 'Choice 1', 100)

		# execute
		has_votes = choice.has_votes()

		# verify
		self.assertTrue(has_votes, 'Expected choice to have votes')
