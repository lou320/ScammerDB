from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from scammers.models import (
    Scammer,
    ScammerName,
    ScammerPhoneNumber,
    ScammerEmail,
    ScammerWebsite,
    ScammerImage,
    Tag,
    ScammerPaymentAccount,
    ScammerProfile
)
from api.serializers import (
    ScammerSerializer,
    ScammerNameSerializer,
    ScammerPhoneNumberSerializer,
    ScammerEmailSerializer,
    ScammerWebsiteSerializer,
    ScammerImageSerializer,
    TagSerializer,
    ScammerPaymentAccountSerializer,
    ScammerProfileSerializer
)

class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        # Search across related models
        name_scammers = ScammerName.objects.filter(name__icontains=query).values_list('scammer_id', flat=True)
        phone_scammers = ScammerPhoneNumber.objects.filter(phone_number__icontains=query).values_list('scammer_id', flat=True)
        email_scammers = ScammerEmail.objects.filter(email__icontains=query).values_list('scammer_id', flat=True)
        website_scammers = ScammerWebsite.objects.filter(website__icontains=query).values_list('scammer_id', flat=True)
        payment_scammers = ScammerPaymentAccount.objects.filter(account_number__icontains=query).values_list('scammer_id', flat=True)
        tag_scammers = Tag.objects.filter(name__icontains=query).values_list('scammer', flat=True)

        # Search in Scammer model itself
        description_scammers = Scammer.objects.filter(description__icontains=query).values_list('id', flat=True)

        # Combine all scammer ids
        scammer_ids = set(list(name_scammers) + list(phone_scammers) + list(email_scammers) + list(website_scammers) + list(payment_scammers) + list(tag_scammers) + list(description_scammers))

        # Get unique Scammer objects
        queryset = Scammer.objects.filter(id__in=scammer_ids)

        serializer = ScammerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class ScammerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scammer.objects.all()
    serializer_class = ScammerSerializer

class ScammerNameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerName.objects.all()
    serializer_class = ScammerNameSerializer

class ScammerPhoneNumberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerPhoneNumber.objects.all()
    serializer_class = ScammerPhoneNumberSerializer

class ScammerEmailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerEmail.objects.all()
    serializer_class = ScammerEmailSerializer

class ScammerWebsiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerWebsite.objects.all()
    serializer_class = ScammerWebsiteSerializer

class ScammerImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerImage.objects.all()
    serializer_class = ScammerImageSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ScammerPaymentAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerPaymentAccount.objects.all()
    serializer_class = ScammerPaymentAccountSerializer

class ScammerProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScammerProfile.objects.all()
    serializer_class = ScammerProfileSerializer
