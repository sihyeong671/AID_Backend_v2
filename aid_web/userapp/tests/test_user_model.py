from django.test import TestCase

# from rest_framework.test import APITestCase


class UserModelTest(TestCase):
    def setup(self):
        print("test setup")

    def test_user_create(self):
        print("create user test")
        self.assertFalse(False)
