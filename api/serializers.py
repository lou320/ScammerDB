from rest_framework import serializers
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

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ScammerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScammerName
        fields = ['id', 'name']

class ScammerPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScammerPhoneNumber
        fields = ['id', 'phone_number']

class ScammerEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScammerEmail
        fields = ['id', 'email']

class ScammerWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScammerWebsite
        fields = ['id', 'website']

class ScammerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScammerImage
        fields = ['id', 'image']

class ScammerPaymentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScammerPaymentAccount
        fields = ['id', 'account_number']

class ScammerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='scammer-detail')
    tags = TagSerializer(many=True, read_only=True)
    names = ScammerNameSerializer(many=True, read_only=True)
    phone_numbers = ScammerPhoneNumberSerializer(many=True, read_only=True)
    emails = ScammerEmailSerializer(many=True, read_only=True)
    websites = ScammerWebsiteSerializer(many=True, read_only=True)
    images = ScammerImageSerializer(many=True, read_only=True)
    payment_accounts = ScammerPaymentAccountSerializer(many=True, read_only=True)
    related_scammers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Scammer
        fields = [
            'url', 'id', 'status', 'description', 'created_at', 'approved_at',
            'tags', 'related_scammers', 'names', 'phone_numbers', 'emails',
            'websites', 'images', 'payment_accounts'
        ]

class ScammerProfileSerializer(serializers.ModelSerializer):
    cases = ScammerSerializer(many=True, read_only=True)

    class Meta:
        model = ScammerProfile
        fields = ['id', 'name', 'image', 'cases']
