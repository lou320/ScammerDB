from django.contrib import admin
from django.utils import timezone
from .models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, ScammerImage, Tag, ScammerPaymentAccount, ScammerCustomField, ScammerProfile

class ScammerNameInline(admin.TabularInline):
    model = ScammerName
    extra = 1

class ScammerPhoneNumberInline(admin.TabularInline):
    model = ScammerPhoneNumber
    extra = 1

class ScammerEmailInline(admin.TabularInline):
    model = ScammerEmail
    extra = 1

class ScammerWebsiteInline(admin.TabularInline):
    model = ScammerWebsite
    extra = 1

class ScammerImageInline(admin.TabularInline):
    model = ScammerImage
    extra = 1

class ScammerPaymentAccountInline(admin.TabularInline):
    model = ScammerPaymentAccount
    extra = 1



@admin.register(Scammer)
class ScammerAdmin(admin.ModelAdmin):
    inlines = [
        ScammerNameInline,
        ScammerPhoneNumberInline,
        ScammerEmailInline,
        ScammerWebsiteInline,
        ScammerImageInline,
        ScammerPaymentAccountInline,
    ]
    list_display = ('__str__', 'status', 'description', 'created_at')
    list_filter = ('status',)
    search_fields = ('names__name', 'phone_numbers__phone_number', 'emails__email', 'websites__website', 'payment_accounts__account_number', 'description')
    filter_horizontal = ('tags',)
    actions = ['make_approved', 'make_rejected']

    def make_approved(self, request, queryset):
        queryset.update(status='approved', approved_at=timezone.now())
    make_approved.short_description = "Mark selected scammers as Approved"

    def make_rejected(self, request, queryset):
        queryset.update(status='rejected', approved_at=None)
    make_rejected.short_description = "Mark selected scammers as Rejected"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(ScammerProfile)
class ScammerProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('cases',)
