from django.core.management.base import BaseCommand
from candidates import Candidate  # Update with your actual app name

class Command(BaseCommand):
    help = 'Change the source field of all candidates to "recruiter"'

    def handle(self, *args, **kwargs):
        try:
            Candidate.objects.update(source='recruiter')
            self.stdout.write(self.style.SUCCESS('Successfully updated source field to "recruiter" for all candidates.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))