from django.test import TestCase

from .models import (
    Attachment,
    Publication,
    Step,
)
from actor.models import (
    Actor,
    Group,
)


class TestPublicationModel(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        pass

    def test_json_repr(self):
        pass


class TestStepModel(TestCase):

    def setUp(self):
        pass

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
        pass

    def test_json_repr(self):
        pass


class TestAttachment(TestCase):

    def setUp(self):
        pass

    def test_str(self):
        pass

    def test_json_repr(self):
        pass
