# Tests for Django admin modifications

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    # Apparently its setUp & not set_up ...
    def setUp(self):
        # Allows us to make http requests
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        # Force authentication. Every http request will have
        # the above credentials as the authenticated user.
        self.client.force_login(self.admin_user)

        # Create a user for us to display on our lists of user.
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )

    def test_users_list(self):
        # A page that displays a list of users.
        # Use reverse to get the url of change list
        # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
