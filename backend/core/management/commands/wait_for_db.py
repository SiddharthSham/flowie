import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        conn_alive_start = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.cursor().execute('SELECT 1')
                if not conn_alive_start:
                    conn_alive_start = time.time()
                break
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 5 second...")
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS('Database available!'))
