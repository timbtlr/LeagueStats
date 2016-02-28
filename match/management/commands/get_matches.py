from django.core.management.base import BaseCommand, CommandError
from match.tasks import schedule_pull_matches

class Command(BaseCommand):
    help = 'Starts a task to pull match data for all summoners'

    def handle(self, *args, **options):
        schedule_pull_matches()