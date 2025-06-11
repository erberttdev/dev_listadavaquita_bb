from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Exibe as migrações aplicadas e pendentes'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name;")
            rows = cursor.fetchall()

        self.stdout.write("Migrações Aplicadas:\n")
        for row in rows:
            self.stdout.write(f"- {row[0]}.{row[1]}\n")
