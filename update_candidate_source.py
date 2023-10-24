from django.core.management.base import BaseCommand
from candidates.models import Candidate  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Update source field for all candidates from "application" to "recruiter"'

    def handle(self, *args, **options):
        # Get all candidates with source='application'
        candidates_to_update = Candidate.objects.filter(source='application')

        # Update the source for each candidate and save it
        for candidate in candidates_to_update:
            candidate.source = 'recruiter'
            candidate.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated source for candidates.'))

