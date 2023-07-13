from django.core.management.base import BaseCommand
from bc.helpers import helper


class Command(BaseCommand):
    help = 'Update last_done field on Stuff models'

    def handle(self, *args, **options):
        # Get the latest done_on value for each StuffRecord
        if helper.updateLatestDone('all'):
            self.stdout.write(self.style.SUCCESS(
                'Last done dates updated successfully'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                'Operation failed!'
            ))
