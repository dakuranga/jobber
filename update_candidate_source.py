import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Replace 'your_project' with your actual project name

# Initialize Django
django.setup()

# Now you can import your models and run your update script
from candidates.models import Candidate  # Replace 'candidates' with your app name

# Your update script here
# Get all candidates with source='application'
candidates_to_update = Candidate.objects.filter(source='application')

# Update the source for each candidate and save it
for candidate in candidates_to_update:
    candidate.source = 'recruiter'
    candidate.save()

print('Successfully updated source for candidates.')
