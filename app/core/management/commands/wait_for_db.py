# To fix db race condition and ensure that the db is ready and available.
# File allows us to run the command through manage.py
import time
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Logs a message when our command is ran
        self.stdout.write("Waiting for database ...")
        db_up = False
        retry = 1
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting for 1 second & retrying for %d times" % retry)
                retry += 1
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("=== Database is available ==="))