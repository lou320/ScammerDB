from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from scammers.models import (
    Scammer, ScammerEmail, ScammerPhoneNumber, ScammerWebsite,
    ScammerPaymentAccount, ScammerCustomField, FieldAccess
)

class Command(BaseCommand):
    help = 'Populates the FieldAccess model for all Scammer-related fields, setting them to public by default.'

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate FieldAccess model...")

        models_to_process = {
            Scammer: ['description', 'status'],
            ScammerEmail: ['email'],
            ScammerPhoneNumber: ['phone_number'],
            ScammerWebsite: ['url'],
            ScammerPaymentAccount: ['account_details'],
            ScammerCustomField: ['name', 'value']
        }

        for model, fields in models_to_process.items():
            model_name_str = model.__name__
            for field_name in fields:
                field_access, created = FieldAccess.objects.get_or_create(
                    model_name=model_name_str,
                    field_name=field_name,
                    defaults={'access_level': 'public'}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created public FieldAccess for {model.__name__}.{field_name}"
                        )
                    )
                else:
                    self.stdout.write(
                        f"FieldAccess for {model.__name__}.{field_name} already exists."
                    )

        self.stdout.write(self.style.SUCCESS("Successfully populated FieldAccess model."))
