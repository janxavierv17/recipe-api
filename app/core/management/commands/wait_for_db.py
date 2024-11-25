# To fix db race condition and ensure that the db is ready and available.
# File allows us to run the command through manage.py
import time
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Initial log message indicating the start of the process
        self.stdout.write("Waiting for database to be ready...")

        db_up = False
        retry = 1
        while not db_up:
            try:
                # Check if the database is available
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                # Log retry attempts with more detail
                self.stdout.write(f"DB unavailable. Retry attempt {retry}...")
                retry += 1
                time.sleep(1)

        # Log a success message when the database is available
        self.stdout.write(self.style.SUCCESS("=== Database is available ==="))
