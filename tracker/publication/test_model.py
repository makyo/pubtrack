from django.test import TestCase

from .models import (
    # Attachment,
    Publication,
    Step,
)
from actor.models import (
    Actor,
    # Group,
)


class TestPublicationModel(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.actor1 = Actor(
            name='Rose Tyler',
            actor_type='author',
            pseudonym='Rose')
        cls.actor1.save()

    @classmethod
    def tearDownClass(cls):
        cls.actor1.delete()

    def setUp(self):
        self.pub1 = Publication(
            title='Doctors and how to date them',
            creator=self.actor1,
            publication_type='book')
        self.pub1.save()

    def test_str(self):
        self.assertEqual(
            str(self.pub1),
            'Publication: Doctors and how to date them '
            '(Book) by Rose Tyler (Author)')

    def test_json_repr(self):
        pass


class TestStepModel(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.actor1 = Actor(
            name='Rose Tyler',
            actor_type='author',
            pseudonym='Rose')
        cls.actor1.save()

    @classmethod
    def tearDownClass(cls):
        cls.actor1.delete()

    def setUp(self):
        self.pub1 = Publication(
            title='Doctors and how to date them',
            creator=self.actor1,
            publication_type='book')
        self.pub1.save()

    def test_save_no_prev_step(self):
        pass

    def test_save_force(self):
        pass

    def test_save_fail_final(self):
        pass

    def test_save_fail_reverse(self):
        pass

    def test_save_fail_flow(self):
        pass

    def test_str(self):
        step = Step(
            publication=self.pub1,
            step_type='query_received')
        step.save()
        self.assertEqual(
            str(step),
            'Step: Query received for Doctors and how to date them')

    def test_json_repr(self):
        pass


class TestAttachment(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        pass

    def test_json_repr(self):
        pass
