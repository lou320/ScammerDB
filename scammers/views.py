from django.shortcuts import render, redirect, get_object_or_404

from django.db import transaction
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, ScammerImage, Tag
from .forms import ScammerForm, ScammerNameFormSet, ScammerPhoneNumberFormSet, ScammerEmailFormSet, ScammerWebsiteFormSet, ScammerImageFormSet, ScammerPaymentAccountFormSet

from django.core.paginator import Paginator


def scammer_list(request):
    query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'all')
    scammers_list = Scammer.objects.filter(status='approved').order_by('-approved_at')

    # If search_field is 'all' but query starts with 'tag:',
    # override search_field and extract the tag name.
    if search_field == 'all' and query.startswith('tag:'):
        search_field = 'tag'
        query = query[len('tag:'):] # Extract the actual tag name

    if query:
        if search_field == 'name':
            scammers_list = scammers_list.filter(names__name__icontains=query).distinct()
        elif search_field == 'phone':
            query = query.lstrip('0')
            scammers_list = scammers_list.filter(phone_numbers__phone_number__icontains=query).distinct()
        elif search_field == 'email':
            scammers_list = scammers_list.filter(emails__email__icontains=query).distinct()
        elif search_field == 'website':
            scammers_list = scammers_list.filter(websites__website__icontains=query).distinct()
        elif search_field == 'tag':
            scammers_list = scammers_list.filter(tags__name__icontains=query).distinct()
        else: # 'all'
            # Create a modified query for phone number search without leading zeros
            phone_query_no_leading_zeros = query.lstrip('0')
            scammers_list = scammers_list.filter(
                Q(names__name__icontains=query) |
                Q(description__icontains=query) |
                Q(phone_numbers__phone_number__icontains=phone_query_no_leading_zeros) |
                Q(emails__email__icontains=query) |
                Q(websites__website__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

    paginator = Paginator(scammers_list, 9) # 9 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate pagination window
    window_size = 1
    current_page = page_obj.number
    total_pages = paginator.num_pages
    
    start = max(current_page - window_size, 1)
    end = min(current_page + window_size, total_pages)

    if start == 1:
        end = min(start + (window_size * 2), total_pages)
    if end == total_pages:
        start = max(end - (window_size * 2), 1)

    page_numbers = range(start, end + 1)

    context = {
        'page_obj': page_obj,
        'query': query,
        'search_field': search_field,
        'page_numbers': page_numbers,
    }
    return render(request, 'scammers/scammer_list.html', context)

from .models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, ScammerImage, Tag, UserScammerAccess
from django.conf import settings

def scammer_detail(request, pk):
    if request.user.is_staff:
        scammer = get_object_or_404(Scammer, pk=pk)
    else:
        scammer = get_object_or_404(Scammer, pk=pk, status='approved')
    
    from_page = request.GET.get('from')
    
    has_access = False
    if request.user.is_staff or getattr(settings, 'FREE_TRIAL_ENABLED', False):
        has_access = True
    elif request.user.is_authenticated:
        has_access = UserScammerAccess.objects.filter(user=request.user, scammer=scammer).exists()

    # Prepare related scammers data for the template
    related_data = []
    if scammer.related_scammers.exists():
        approved_related_scammers = scammer.related_scammers.filter(status='approved')
        for related in approved_related_scammers:
            reasons = scammer.get_relationship_reasons(related)
            related_data.append({'scammer': related, 'reasons': reasons})

    # Prepare display values for sensitive fields
    display_phone_numbers = []
    for phone in scammer.phone_numbers.all():
        display_phone_numbers.append({'value': phone.get_display_value(has_access), 'is_masked': not has_access})

    display_emails = []
    for email in scammer.emails.all():
        display_emails.append({'value': email.get_display_value(has_access), 'is_masked': not has_access})

    display_websites = []
    for website in scammer.websites.all():
        display_websites.append({'value': website.get_display_value(has_access), 'is_masked': not has_access})

    display_payment_accounts = []
    for account in scammer.payment_accounts.all():
        display_payment_accounts.append({'value': account.get_display_value(has_access), 'is_masked': not has_access})

    display_images = []
    for image in scammer.images.all():
        display_images.append({'url': image.get_display_image_url(has_access), 'is_masked': not has_access})

    context = {
        'scammer': scammer,
        'from_page': from_page,
        'has_access': has_access,
        'related_data': related_data,
        'display_phone_numbers': display_phone_numbers,
        'display_emails': display_emails,
        'display_websites': display_websites,
        'display_payment_accounts': display_payment_accounts,
        'display_images': display_images,
    }
    return render(request, 'scammers/scammer_detail.html', context)

def add_scammer(request):
    if request.method == 'POST':
        form = ScammerForm(request.POST, request.FILES)
        name_formset = ScammerNameFormSet(request.POST, prefix='names')
        phone_formset = ScammerPhoneNumberFormSet(request.POST, prefix='phones')
        email_formset = ScammerEmailFormSet(request.POST, prefix='emails')
        website_formset = ScammerWebsiteFormSet(request.POST, prefix='websites')
        image_formset = ScammerImageFormSet(request.POST, request.FILES, prefix='images')
        payment_account_formset = ScammerPaymentAccountFormSet(request.POST, prefix='payment_accounts')

        if (form.is_valid() and name_formset.is_valid() and phone_formset.is_valid() and
            email_formset.is_valid() and website_formset.is_valid() and image_formset.is_valid() and
            payment_account_formset.is_valid()):
            with transaction.atomic():
                scammer = form.save()
                
                name_formset.instance = scammer
                name_formset.save()
                
                phone_formset.instance = scammer
                phone_formset.save()

                email_formset.instance = scammer
                email_formset.save()

                website_formset.instance = scammer
                website_formset.save()

                image_formset.instance = scammer
                image_formset.save()

                payment_account_formset.instance = scammer
                payment_account_formset.save()

                # Process tags
                tag_string = form.cleaned_data.get('tags', '')
                if tag_string:
                    try:
                        import json
                        tag_data = json.loads(tag_string)
                        tag_names = [tag['value'] for tag in tag_data]
                        
                        scammer.tags.clear()
                        for tag_name in tag_names:
                            tag, created = Tag.objects.get_or_create(name=tag_name)
                            scammer.tags.add(tag)
                    except (json.JSONDecodeError, TypeError):
                        # Fallback for simple string, though not expected with Tagify
                        tag_names = [name.strip() for name in tag_string.split(',') if name.strip()]
                        for tag_name in tag_names:
                            tag, created = Tag.objects.get_or_create(name=tag_name)
                            scammer.tags.add(tag)

            return redirect('scammer_list')
    else:
        form = ScammerForm()
        name_formset = ScammerNameFormSet(prefix='names')
        phone_formset = ScammerPhoneNumberFormSet(prefix='phones')
        email_formset = ScammerEmailFormSet(prefix='emails')
        website_formset = ScammerWebsiteFormSet(prefix='websites')
        image_formset = ScammerImageFormSet(prefix='images')
        payment_account_formset = ScammerPaymentAccountFormSet(prefix='payment_accounts')

    all_tags = list(Tag.objects.values_list('name', flat=True))
    context = {
        'form': form,
        'name_formset': name_formset,
        'phone_formset': phone_formset,
        'email_formset': email_formset,
        'website_formset': website_formset,
        'image_formset': image_formset,
        'payment_account_formset': payment_account_formset,
        'all_tags': all_tags,
    }
    return render(request, 'scammers/add_scammer.html', context)

def contact_us(request):
    return render(request, 'scammers/contact_us.html')

@staff_member_required
def approve_scammer(request, pk):
    scammer = get_object_or_404(Scammer, pk=pk)
    scammer.status = 'approved'
    scammer.approved_at = timezone.now()
    scammer.save()
    return redirect('scammer_detail', pk=pk)

@staff_member_required
def reject_scammer(request, pk):
    scammer = get_object_or_404(Scammer, pk=pk)
    scammer.status = 'rejected'
    scammer.approved_at = None
    scammer.save()
    return redirect('scammer_detail', pk=pk)

@staff_member_required
def pending_scammers(request):
    scammers_list = Scammer.objects.filter(status='pending').order_by('-created_at')
    paginator = Paginator(scammers_list, 12) # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate pagination window
    window_size = 1
    current_page = page_obj.number
    total_pages = paginator.num_pages
    
    start = max(current_page - window_size, 1)
    end = min(current_page + window_size, total_pages)

    if start == 1:
        end = min(start + (window_size * 2), total_pages)
    if end == total_pages:
        start = max(end - (window_size * 2), 1)

    page_numbers = range(start, end + 1)

    context = {
        'page_obj': page_obj,
        'page_numbers': page_numbers,
    }
    return render(request, 'scammers/pending_scammer_list.html', context)

from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'scammers/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def purchase_access(request, pk):
    scammer = get_object_or_404(Scammer, pk=pk)
    UserScammerAccess.objects.get_or_create(user=request.user, scammer=scammer)
    return redirect('scammer_detail', pk=pk)
