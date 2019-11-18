from django.core.management.base import BaseCommand, CommandError
from match.tasks import collect_all_new_matches

class Command(BaseCommand):
    help = 'Starts a task to pull match data for all summoners'

    def handle(self, *args, **options):
        collect_all_new_matches()