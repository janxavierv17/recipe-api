# Tests for models
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


def create_superuser(**kwargs):
    return get_user_model().objects.create_superuser(**kwargs)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"
        user = create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = create_user(email=email, password="sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            create_user(email="", password="test123")

    def test_create_superuser(self):
        user = create_superuser(email="test@example.com", password="test123")

        # is_superuser is provided by PermissionsMixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_new_superuser_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            create_superuser(email="", password="test123")

    def test_create_recipe(self):
        user = create_user(email="test@example.com", password="testpass123")
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user(email="test@example.com", password="test123")
        tag = models.Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)
