import random
from django.core.management.base import BaseCommand
from faker import Faker
from scammers.models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, Tag

class Command(BaseCommand):
    help = 'Populates the database with a specified number of fake scammers.'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, help='The number of scammers to create.', default=50)

    def handle(self, *args, **options):
        fake = Faker()
        number_of_scammers = options['number']

        self.stdout.write(self.style.SUCCESS(f'--- Clearing old data ---'))
        Scammer.objects.all().delete()
        Tag.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f'--- Creating new tags ---'))
        tag_list = [
            'Phishing', 'Romance Scam', 'Tech Support', 'Investment', 'Lottery', 
            'Impersonation', 'Charity Fraud', 'Job Offer', 'Fake Antivirus', 'Grandparent Scam'
        ]
        tags = [Tag.objects.create(name=tag_name) for tag_name in tag_list]

        self.stdout.write(self.style.SUCCESS(f'--- Creating {number_of_scammers} new scammers ---'))

        for _ in range(number_of_scammers):
            # Create Scammer
            scammer = Scammer.objects.create(
                description=fake.paragraph(nb_sentences=5)
            )

            # Add Names
            for _ in range(random.randint(1, 3)):
                ScammerName.objects.create(scammer=scammer, name=fake.name())

            # Add Phone Numbers
            for _ in range(random.randint(1, 4)):
                ScammerPhoneNumber.objects.create(scammer=scammer, phone_number=fake.phone_number())

            # Add Emails
            for _ in range(random.randint(1, 2)):
                ScammerEmail.objects.create(scammer=scammer, email=fake.email())

            # Add Websites
            for _ in range(random.randint(0, 2)):
                ScammerWebsite.objects.create(scammer=scammer, website=fake.url())

            # Assign Tags
            num_tags = random.randint(1, 4)
            scammer.tags.set(random.sample(tags, num_tags))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {number_of_scammers} scammers.'))
