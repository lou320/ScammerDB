from django.shortcuts import render, redirect, get_object_or_404

from django.db import transaction
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, ScammerImage, Tag, ScammerProfile
from .forms import ScammerForm, ScammerNameFormSet, ScammerPhoneNumberFormSet, ScammerEmailFormSet, ScammerWebsiteFormSet, ScammerImageFormSet, ScammerPaymentAccountFormSet, ScammerProfileForm


from django.core.paginator import Paginator


def scammer_list(request):
    query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'all')
    
    # Start with an empty queryset
    scammers_list = Scammer.objects.none()

    if query:
        # Perform search on Scammer model
        scammer_q = Scammer.objects.filter(status='approved')
        if search_field == 'name':
            scammer_q = scammer_q.filter(names__name__icontains=query)
        elif search_field == 'phone':
            query_no_leading_zeros = query.lstrip('0')
            scammer_q = scammer_q.filter(phone_numbers__phone_number__icontains=query_no_leading_zeros)
        elif search_field == 'email':
            scammer_q = scammer_q.filter(emails__email__icontains=query)
        elif search_field == 'website':
            scammer_q = scammer_q.filter(websites__website__icontains=query)
        elif search_field == 'tag':
            scammer_q = scammer_q.filter(tags__name__icontains=query)
        else: # 'all'
            phone_query_no_leading_zeros = query.lstrip('0')
            scammer_q = scammer_q.filter(
                Q(names__name__icontains=query) |
                Q(description__icontains=query) |
                Q(phone_numbers__phone_number__icontains=phone_query_no_leading_zeros) |
                Q(emails__email__icontains=query) |
                Q(websites__website__icontains=query) |
                Q(tags__name__icontains=query)
            )
        
        # Perform search on ScammerProfile model
        profile_q = ScammerProfile.objects.filter(name__icontains=query)
        
        # Get cases from matching profiles
        profile_scammers = Scammer.objects.filter(profiles__in=profile_q, status='approved')
        
        # Combine the querysets and remove duplicates
        scammers_list = (scammer_q | profile_scammers).distinct().order_by('-approved_at')

    else:
        scammers_list = Scammer.objects.filter(status='approved').order_by('-approved_at')


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

    # Get the first associated profile, if any
    profile = scammer.profiles.first()

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
        'profile': profile,
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

@staff_member_required
def add_scammer_profile(request):
    if request.method == 'POST':
        form = ScammerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()

            case_ids_string = form.cleaned_data.get('cases', '')
            if case_ids_string:
                try:
                    import json
                    case_data = json.loads(case_ids_string)
                    case_ids = [item['value'] for item in case_data]
                    
                    profile.cases.clear()
                    for case_id in case_ids:
                        try:
                            scammer = Scammer.objects.get(id=case_id)
                            profile.cases.add(scammer)
                        except Scammer.DoesNotExist:
                            # Handle case where an invalid ID is entered
                            pass
                except (json.JSONDecodeError, TypeError):
                    # Fallback for simple comma-separated string
                    case_ids = [id.strip() for id in case_ids_string.split(',') if id.strip()]
                    profile.cases.clear()
                    for case_id in case_ids:
                        try:
                            scammer = Scammer.objects.get(id=case_id)
                        except (Scammer.DoesNotExist, ValueError):
                            # Handle invalid ID or non-integer
                            pass
            
            return redirect('scammer_profile_list')
    else:
        form = ScammerProfileForm()

    all_case_ids = list(Scammer.objects.values_list('id', flat=True))
    context = {
        'form': form,
        'all_case_ids': all_case_ids,
    }
    return render(request, 'scammers/add_scammer_profile.html', context)


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

from django.views.generic import ListView, DetailView
from .models import ScammerProfile

class ScammerProfileListView(ListView):
    model = ScammerProfile
    template_name = 'scammers/scammer_profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 9

class ScammerProfileDetailView(DetailView):
    model = ScammerProfile
    template_name = 'scammers/scammer_profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Get approved cases
        approved_cases = profile.cases.filter(status='approved').order_by('-approved_at')
        context['cases'] = approved_cases
        
        # Initialize sets to store unique details
        all_names = set()
        all_phone_numbers = set()
        all_emails = set()
        all_websites = set()
        all_payment_accounts = set()
        all_tags = set()
        
        # Aggregate details from all approved cases
        for case in approved_cases:
            for name in case.names.all():
                if name.name:
                    all_names.add(name.name)
            for phone in case.phone_numbers.all():
                if phone.phone_number:
                    all_phone_numbers.add(phone.phone_number)
            for email in case.emails.all():
                if email.email:
                    all_emails.add(email.email)
            for website in case.websites.all():
                if website.website:
                    all_websites.add(website.website)
            for account in case.payment_accounts.all():
                if account.account_number:
                    all_payment_accounts.add(account.account_number)
            for tag in case.tags.all():
                if tag.name:
                    all_tags.add(tag.name)
                    
        context['all_names'] = sorted(list(all_names))
        context['all_phone_numbers'] = sorted(list(all_phone_numbers))
        context['all_emails'] = sorted(list(all_emails))
        context['all_websites'] = sorted(list(all_websites))
        context['all_payment_accounts'] = sorted(list(all_payment_accounts))
        context['all_tags'] = sorted(list(all_tags))
        
        return context