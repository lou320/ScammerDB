from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerPaymentAccount

def link_related_scammers(instance, field_name):
    """
    Finds and links scammers who share the same data point (e.g., phone number, email).
    
    :param instance: The model instance that was just saved (e.g., ScammerPhoneNumber).
    :param field_name: The name of the field to check for matches (e.g., 'phone_number').
    """
    try:
        # Get the value of the field from the instance
        value = getattr(instance, field_name)
        if not value:
            return

        # The scammer profile that triggered the signal
        source_scammer = instance.scammer

        # Find all other instances of the same model with the same value (case-insensitive),
        # excluding the one that was just saved.
        filter_kwargs = {f'{field_name}__iexact': value}
        related_instances = instance.__class__.objects.filter(**filter_kwargs).exclude(pk=instance.pk)

        # Get the Scammer objects linked to these instances
        related_scammers = Scammer.objects.filter(
            pk__in=related_instances.values_list('scammer_id', flat=True)
        ).exclude(pk=source_scammer.pk)

        # Link them
        for related_scammer in related_scammers:
            source_scammer.related_scammers.add(related_scammer)
            # The relationship is symmetrical, so this is not strictly needed
            # but it makes the connection explicit.
            related_scammer.related_scammers.add(source_scammer)

    except Exception as e:
        # It's often best not to crash the save operation due to a linking error.
        # You might want to log this error instead.
        print(f"Error in linking scammers: {e}")


@receiver(post_save, sender=ScammerPhoneNumber)
def handle_phone_number_save(sender, instance, created, **kwargs):
    link_related_scammers(instance, 'phone_number')

@receiver(post_save, sender=ScammerEmail)
def handle_email_save(sender, instance, created, **kwargs):
    link_related_scammers(instance, 'email')

@receiver(post_save, sender=ScammerName)
def handle_name_save(sender, instance, created, **kwargs):
    link_related_scammers(instance, 'name')

@receiver(post_save, sender=ScammerPaymentAccount)
def handle_payment_account_save(sender, instance, created, **kwargs):
    link_related_scammers(instance, 'account_number')