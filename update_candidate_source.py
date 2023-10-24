from candidates.models import Candidate

# Get all candidates with source='application'
candidates_to_update = Candidate.objects.filter(source='application')

# Update the source for each candidate and save it
for candidate in candidates_to_update:
    candidate.source = 'recruiter'
    candidate.save()

