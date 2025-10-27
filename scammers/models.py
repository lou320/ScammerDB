from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings

class Scammer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    related_scammers = models.ManyToManyField('self', blank=True)

    def __str__(self):
        first_name = self.names.first()
        return first_name.name if first_name else f"Scammer #{self.pk}"

    def get_relationship_reasons(self, other_scammer):
        reasons = []
        # Compare phone numbers (case-insensitive)
        self_phones = set(p.lower() for p in self.phone_numbers.values_list('phone_number', flat=True) if p)
        other_phones = set(p.lower() for p in other_scammer.phone_numbers.values_list('phone_number', flat=True) if p)
        common_phones = self_phones.intersection(other_phones)
        for phone in common_phones:
            reasons.append(f"{_('Phone')}: {phone}")

        # Compare emails (case-insensitive)
        self_emails = set(e.lower() for e in self.emails.values_list('email', flat=True) if e)
        other_emails = set(e.lower() for e in other_scammer.emails.values_list('email', flat=True) if e)
        common_emails = self_emails.intersection(other_emails)
        for email in common_emails:
            reasons.append(f"{_('Email')}: {email}")

        # Compare names (case-insensitive)
        self_names = set(n.lower() for n in self.names.values_list('name', flat=True) if n)
        other_names = set(n.lower() for n in other_scammer.names.values_list('name', flat=True) if n)
        common_names = self_names.intersection(other_names)
        for name in common_names:
            reasons.append(f"{_('Name')}: {name}")

        # Compare payment accounts (case-insensitive)
        self_accounts = set(a.lower() for a in self.payment_accounts.values_list('account_number', flat=True) if a)
        other_accounts = set(a.lower() for a in other_scammer.payment_accounts.values_list('account_number', flat=True) if a)
        common_accounts = self_accounts.intersection(other_accounts)
        for account in common_accounts:
            reasons.append(f"{_('Account')}: {account}")
            
        return reasons

class ScammerName(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='names', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class ScammerPhoneNumber(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='phone_numbers', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.phone_number

    def get_display_value(self, has_access):
        if has_access or not self.phone_number:
            return self.phone_number
        # Mask phone number: show country code + first 2-3 digits, then asterisks
        if len(self.phone_number) > 5:
            return self.phone_number[:5] + '*' * (len(self.phone_number) - 5)
        return '*' * len(self.phone_number)

class ScammerEmail(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.email

    def get_display_value(self, has_access):
        if has_access or not self.email:
            return self.email
        # Mask email: show first 2-3 chars, then asterisks, then part of domain
        parts = self.email.split('@')
        if len(parts) == 2:
            username = parts[0]
            domain = parts[1]
            masked_username = username[:2] + '*' * (len(username) - 2) if len(username) > 2 else '*' * len(username)
            masked_domain = domain[:2] + '*' * (len(domain) - 2) if len(domain) > 2 else '*' * len(domain)
            return f"{masked_username}@{masked_domain}"
        return '*' * len(self.email)

class ScammerWebsite(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='websites', on_delete=models.CASCADE)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.website

    def get_display_value(self, has_access):
        if has_access or not self.website:
            return self.website
        # Mask website: show protocol, then mask part of domain
        if '://' in self.website:
            protocol, rest = self.website.split('://', 1)
            if '.' in rest:
                domain_parts = rest.split('.')
                masked_domain = domain_parts[0][:2] + '*' * (len(domain_parts[0]) - 2) if len(domain_parts[0]) > 2 else '*' * len(domain_parts[0])
                return f"{protocol}://{masked_domain}.{domain_parts[-1]}"
            return f"{protocol}://{'' * len(rest)}"
        return '*' * len(self.website)

class ScammerImage(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scammer_images/', blank=True, null=True)

    def __str__(self):
        return self.image.name

    def get_display_image_url(self, has_access):
        if has_access and self.image:
            return self.image.url
        # Return URL to default image if not purchased or no image
        current_language = get_language()
        if current_language == 'my':
            return settings.STATIC_URL + 'images/default_unpurchased_image_my.png'
        else: # Default to English or a generic image
            return settings.STATIC_URL + 'images/default_unpurchased_image_en.png'

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ScammerPaymentAccount(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='payment_accounts', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.account_number

    def get_display_value(self, has_access):
        if has_access or not self.account_number:
            return self.account_number
        # Mask account number: show only last 4 digits
        if len(self.account_number) > 4:
            return '*' * (len(self.account_number) - 4) + self.account_number[-4:]
        return '*' * len(self.account_number)

class ScammerCustomField(models.Model):
    scammer = models.ForeignKey(Scammer, related_name='custom_fields', on_delete=models.CASCADE)
    field_label = models.CharField(max_length=255)
    field_value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.field_label}: {self.field_value}"

from django.contrib.auth.models import User

class UserScammerAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scammer = models.ForeignKey(Scammer, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'scammer')

    def __str__(self):
        return f"{self.user.username} has access to {self.scammer}"

class FieldAccess(models.Model):
    ACCESS_CHOICES = [
        ('public', 'Public'),
        ('premium', 'Premium'),
    ]
    model_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='public')

    class Meta:
        unique_together = ('model_name', 'field_name')

    def __str__(self):
        return f"{self.model_name}.{self.field_name} - {self.get_access_level_display()}"

class ScammerProfile(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cases = models.ManyToManyField(Scammer, related_name='profiles')

    def __str__(self):
        return self.name
