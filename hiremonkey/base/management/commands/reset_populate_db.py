from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Reset and populate the database with multiple users and profiles"

    def handle(self, *args, **kwargs):
        # First, flush the database to clear all existing data
        self.stdout.write(self.style.SUCCESS("Flushing database..."))
        self.stdout.write("This will delete all existing data!")

        call_command("flush", "--no-input")

        # Create Users
        # self.stdout.write("Creating users...")
        user1 = User.objects.create_superuser(
            username="nautilus", password="rladnwls2001"
        )
        user2 = User.objects.create_superuser(username="azir", password="rladnwls2001")
        user2 = User.objects.create_superuser(
            username="graves", password="rladnwls2001"
        )
        user2 = User.objects.create_superuser(username="kaisa", password="rladnwls2001")

        # Load the fixture data
        self.stdout.write("Loading fixture data...")
        # call_command("loaddata", "sample")  # or your_fixture_file.yaml

        self.stdout.write(self.style.SUCCESS("Database has been reset and populated!"))
