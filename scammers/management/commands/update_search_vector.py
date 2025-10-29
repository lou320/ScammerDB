from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from scammers.models import Scammer

class Command(BaseCommand):
    help = 'Updates the search_vector for all scammers'

    def handle(self, *args, **options):
        self.stdout.write('Updating search vectors...')
        Scammer.objects.update(
            search_vector=(
                SearchVector('names__name', weight='A') +
                SearchVector('description', weight='B') +
                SearchVector('phone_numbers__phone_number', weight='A') +
                SearchVector('emails__email', weight='A') +
                SearchVector('websites__website', weight='B') +
                SearchVector('tags__name', weight='A')
            )
        )
        self.stdout.write(self.style.SUCCESS('Search vectors updated successfully!'))
