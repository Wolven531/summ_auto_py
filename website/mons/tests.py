"""
    This is the tests module for the mons application
"""

# import datetime
from django.test import TestCase
from django.urls import reverse
# from django.utils import timezone
from .models import Monster

class TestUtil():# pylint: disable=R0903
    """
        This method houses utility methods for the tests below
    """

    @staticmethod
    def create_monster(awaken_name):
        """
            Create a monster with the given:
            * awaken_name
        """
        return Monster.objects.create(awaken_name=awaken_name)

class MonsterIndexViewTests(TestCase):
    """
        This class tests the functionality of the Monster index view
    """

    def test_index_should_be_empty_when_no_monster(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there are no monster to display
        """
        # setup
        # execute
        response = self.client.get(reverse('mons:index'))

        # verify
        self.assertContains(response, 'No monsters are available', status_code=200)
        self.assertQuerysetEqual(response.context['monster_list'], [])

    def test_index_should_display_when_one_monster(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there is a monster
        """
        # setup
        mon = TestUtil.create_monster('Blarger')

        # execute
        response = self.client.get(reverse('mons:index'))

        # verify
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['monster_list']), [mon])

    def test_index_should_display_ordered_when_multiple_monsters(self):# pylint: disable=C0103
        """
            This test ensures that the index view displays properly
            when there is more than one monster (and that they are in order)
        """
        # setup
        # NOTE: we create Zeta first because if the view does not order the
        # results, Zeta would default to the first in the list
        mon1 = TestUtil.create_monster('Zeta')
        mon2 = TestUtil.create_monster('Alpha')

        # execute
        response = self.client.get(reverse('mons:index'))

        # verify
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context['monster_list']), [mon2, mon1])

class MonsterDetailViewTests(TestCase):
    """
        This class tests the functionality of the Monster detail view
    """

    def test_detail_should_display(self):# pylint: disable=C0103
        """
            This test ensures the detail view will display
            when a user attempts to view the detail page for a monster
        """
        # setup
        mon = TestUtil.create_monster('Alpha')
        url = reverse('mons:detail', args=[mon.id])

        # execute
        response = self.client.get(url)

        # verify
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monster'], mon)

class MonsterModelTests(TestCase):
    """
        This class tests the functionality of the Monster model
    """
