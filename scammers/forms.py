from django import forms
from django.forms import inlineformset_factory, MultiWidget, Select, TextInput
from django.utils.translation import gettext_lazy as _
from .models import Scammer, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, ScammerImage, Tag, ScammerPaymentAccount, ScammerCustomField, ScammerProfile

COUNTRY_CODE_CHOICES = [
    ('+93', 'AF (+93)'),
    ('+358', 'AX (+358)'),
    ('+355', 'AL (+355)'),
    ('+213', 'DZ (+213)'),
    ('+1-684', 'AS (+1-684)'),
    ('+376', 'AD (+376)'),
    ('+244', 'AO (+244)'),
    ('+1-264', 'AI (+1-264)'),
    ('+672', 'AQ (+672)'),
    ('+1-268', 'AG (+1-268)'),
    ('+54', 'AR (+54)'),
    ('+374', 'AM (+374)'),
    ('+297', 'AW (+297)'),
    ('+61', 'AU (+61)'),
    ('+43', 'AT (+43)'),
    ('+994', 'AZ (+994)'),
    ('+1-242', 'BS (+1-242)'),
    ('+973', 'BH (+973)'),
    ('+880', 'BD (+880)'),
    ('+1-246', 'BB (+1-246)'),
    ('+375', 'BY (+375)'),
    ('+32', 'BE (+32)'),
    ('+501', 'BZ (+501)'),
    ('+229', 'BJ (+229)'),
    ('+1-441', 'BM (+1-441)'),
    ('+975', 'BT (+975)'),
    ('+591', 'BO (+591)'),
    ('+387', 'BA (+387)'),
    ('+267', 'BW (+267)'),
    ('+47', 'BV (+47)'),
    ('+55', 'BR (+55)'),
    ('+1-284', 'VG (+1-284)'),
    ('+246', 'IO (+246)'),
    ('+673', 'BN (+673)'),
    ('+359', 'BG (+359)'),
    ('+226', 'BF (+226)'),
    ('+257', 'BI (+257)'),
    ('+855', 'KH (+855)'),
    ('+237', 'CM (+237)'),
    ('+1', 'CA (+1)'),
    ('+238', 'CV (+238)'),
    ('+1-345', 'KY (+1-345)'),
    ('+236', 'CF (+236)'),
    ('+235', 'TD (+235)'),
    ('+56', 'CL (+56)'),
    ('+86', 'CN (+86)'),
    ('+61', 'CX (+61)'),
    ('+61', 'CC (+61)'),
    ('+57', 'CO (+57)'),
    ('+269', 'KM (+269)'),
    ('+242', 'CG (+242)'),
    ('+243', 'CD (+243)'),
    ('+682', 'CK (+682)'),
    ('+506', 'CR (+506)'),
    ('+385', 'HR (+385)'),
    ('+53', 'CU (+53)'),
    ('+599', 'CW (+599)'),
    ('+357', 'CY (+357)'),
    ('+420', 'CZ (+420)'),
    ('+45', 'DK (+45)'),
    ('+253', 'DJ (+253)'),
    ('+1-767', 'DM (+1-767)'),
    ('+1-809', 'DO (+1-809)'),
    ('+1-829', 'DO (+1-829)'),
    ('+1-849', 'DO (+1-849)'),
    ('+593', 'EC (+593)'),
    ('+20', 'EG (+20)'),
    ('+503', 'SV (+503)'),
    ('+240', 'GQ (+240)'),
    ('+291', 'ER (+291)'),
    ('+372', 'EE (+372)'),
    ('+268', 'SZ (+268)'),
    ('+251', 'ET (+251)'),
    ('+500', 'FK (+500)'),
    ('+298', 'FO (+298)'),
    ('+679', 'FJ (+679)'),
    ('+358', 'FI (+358)'),
    ('+33', 'FR (+33)'),
    ('+594', 'GF (+594)'),
    ('+689', 'PF (+689)'),
    ('+262', 'TF (+262)'),
    ('+241', 'GA (+241)'),
    ('+220', 'GM (+220)'),
    ('+995', 'GE (+995)'),
    ('+49', 'DE (+49)'),
    ('+233', 'GH (+233)'),
    ('+350', 'GI (+350)'),
    ('+30', 'GR (+30)'),
    ('+299', 'GL (+299)'),
    ('+1-473', 'GD (+1-473)'),
    ('+590', 'GP (+590)'),
    ('+1-671', 'GU (+1-671)'),
    ('+502', 'GT (+502)'),
    ('+44-1481', 'GG (+44-1481)'),
    ('+224', 'GN (+224)'),
    ('+245', 'GW (+245)'),
    ('+592', 'GY (+592)'),
    ('+509', 'HT (+509)'),
    ('+672', 'HM (+672)'),
    ('+379', 'VA (+379)'),
    ('+504', 'HN (+504)'),
    ('+852', 'HK (+852)'),
    ('+36', 'HU (+36)'),
    ('+354', 'IS (+354)'),
    ('+91', 'IN (+91)'),
    ('+62', 'ID (+62)'),
    ('+98', 'IR (+98)'),
    ('+964', 'IQ (+964)'),
    ('+353', 'IE (+353)'),
    ('+44-1624', 'IM (+44-1624)'),
    ('+972', 'IL (+972)'),
    ('+39', 'IT (+39)'),
    ('+225', 'CI (+225)'),
    ('+1-876', 'JM (+1-876)'),
    ('+81', 'JP (+81)'),
    ('+44-1534', 'JE (+44-1534)'),
    ('+962', 'JO (+962)'),
    ('+7', 'KZ (+7)'),
    ('+254', 'KE (+254)'),
    ('+686', 'KI (+686)'),
    ('+850', 'KP (+850)'),
    ('+82', 'KR (+82)'),
    ('+965', 'KW (+965)'),
    ('+996', 'KG (+996)'),
    ('+856', 'LA (+856)'),
    ('+371', 'LV (+371)'),
    ('+961', 'LB (+961)'),
    ('+266', 'LS (+266)'),
    ('+231', 'LR (+231)'),
    ('+218', 'LY (+218)'),
    ('+423', 'LI (+423)'),
    ('+370', 'LT (+370)'),
    ('+352', 'LU (+352)'),
    ('+853', 'MO (+853)'),
    ('+261', 'MG (+261)'),
    ('+265', 'MW (+265)'),
    ('+60', 'MY (+60)'),
    ('+960', 'MV (+960)'),
    ('+223', 'ML (+223)'),
    ('+356', 'MT (+356)'),
    ('+692', 'MH (+692)'),
    ('+596', 'MQ (+596)'),
    ('+222', 'MR (+222)'),
    ('+230', 'MU (+230)'),
    ('+262', 'YT (+262)'),
    ('+52', 'MX (+52)'),
    ('+691', 'FM (+691)'),
    ('+373', 'MD (+373)'),
    ('+377', 'MC (+377)'),
    ('+976', 'MN (+976)'),
    ('+382', 'ME (+382)'),
    ('+1-664', 'MS (+1-664)'),
    ('+212', 'MA (+212)'),
    ('+258', 'MZ (+258)'),
    ('+95', 'MM (+95)'),
    ('+264', 'NA (+264)'),
    ('+674', 'NR (+674)'),
    ('+977', 'NP (+977)'),
    ('+31', 'NL (+31)'),
    ('+687', 'NC (+687)'),
    ('+64', 'NZ (+64)'),
    ('+505', 'NI (+505)'),
    ('+227', 'NE (+227)'),
    ('+234', 'NG (+234)'),
    ('+683', 'NU (+683)'),
    ('+672', 'NF (+672)'),
    ('+389', 'MK (+389)'),
    ('+1-670', 'MP (+1-670)'),
    ('+47', 'NO (+47)'),
    ('+968', 'OM (+968)'),
    ('+92', 'PK (+92)'),
    ('+680', 'PW (+680)'),
    ('+970', 'PS (+970)'),
    ('+507', 'PA (+507)'),
    ('+675', 'PG (+675)'),
    ('+595', 'PY (+595)'),
    ('+51', 'PE (+51)'),
    ('+63', 'PH (+63)'),
    ('+64', 'PN (+64)'),
    ('+48', 'PL (+48)'),
    ('+351', 'PT (+351)'),
    ('+1-787', 'PR (+1-787)'),
    ('+1-939', 'PR (+1-939)'),
    ('+974', 'QA (+974)'),
    ('+262', 'RE (+262)'),
    ('+40', 'RO (+40)'),
    ('+7', 'RU (+7)'),
    ('+250', 'RW (+250)'),
    ('+590', 'BL (+590)'),
    ('+290', 'SH (+290)'),
    ('+1-869', 'KN (+1-869)'),
    ('+1-758', 'LC (+1-758)'),
    ('+590', 'MF (+590)'),
    ('+508', 'PM (+508)'),
    ('+1-784', 'VC (+1-784)'),
    ('+685', 'WS (+685)'),
    ('+378', 'SM (+378)'),
    ('+239', 'ST (+239)'),
    ('+966', 'SA (+966)'),
    ('+221', 'SN (+221)'),
    ('+381', 'RS (+381)'),
    ('+248', 'SC (+248)'),
    ('+232', 'SL (+232)'),
    ('+65', 'SG (+65)'),
    ('+1-721', 'SX (+1-721)'),
    ('+421', 'SK (+421)'),
    ('+386', 'SI (+386)'),
    ('+677', 'SB (+677)'),
    ('+252', 'SO (+252)'),
    ('+27', 'ZA (+27)'),
    ('+500', 'GS (+500)'),
    ('+211', 'SS (+211)'),
    ('+34', 'ES (+34)'),
    ('+94', 'LK (+94)'),
    ('+249', 'SD (+249)'),
    ('+597', 'SR (+597)'),
    ('+47', 'SJ (+47)'),
    ('+46', 'SE (+46)'),
    ('+41', 'CH (+41)'),
    ('+963', 'SY (+963)'),
    ('+886', 'TW (+886)'),
    ('+992', 'TJ (+992)'),
    ('+255', 'TZ (+255)'),
    ('+66', 'TH (+66)'),
    ('+670', 'TL (+670)'),
    ('+228', 'TG (+228)'),
    ('+690', 'TK (+690)'),
    ('+676', 'TO (+676)'),
    ('+1-868', 'TT (+1-868)'),
    ('+216', 'TN (+216)'),
    ('+90', 'TR (+90)'),
    ('+993', 'TM (+993)'),
    ('+1-649', 'TC (+1-649)'),
    ('+688', 'TV (+688)'),
    ('+256', 'UG (+256)'),
    ('+380', 'UA (+380)'),
    ('+971', 'AE (+971)'),
    ('+44', 'GB (+44)'),
    ('+1', 'US (+1)'),
    ('+246', 'UM (+246)'),
    ('+699', 'UM (+699)'),
    ('+598', 'UY (+598)'),
    ('+998', 'UZ (+998)'),
    ('+678', 'VU (+678)'),
    ('+58', 'VE (+58)'),
    ('+84', 'VN (+84)'),
    ('+1-284', 'VG (+1-284)'),
    ('+1-340', 'VI (+1-340)'),
    ('+681', 'WF (+681)'),
    ('+212', 'EH (+212)'),
    ('+967', 'YE (+967)'),
    ('+260', 'ZM (+260)'),
    ('+263', 'ZW (+263)'),
]

class PhoneNumberWidget(MultiWidget):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        widgets = [
            Select(attrs={'class': 'form-select country-code-select'}, choices=COUNTRY_CODE_CHOICES),
            TextInput(attrs={'class': 'form-control', 'placeholder': _('Scammer Phone Number')})
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            for code, _ in COUNTRY_CODE_CHOICES:
                if value.startswith(code):
                    return [code, value[len(code):]]
            return ['', value]
        return ['+95', '']

class PhoneNumberField(forms.MultiValueField):
    widget = PhoneNumberWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.ChoiceField(choices=COUNTRY_CODE_CHOICES, initial='+95'),
            forms.CharField(),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            country_code = data_list[0]
            local_number = data_list[1].lstrip('0') # Remove leading '0'
            return f'{country_code}{local_number}'
        return ''

class ScammerForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Comma-separated tags')}),
        help_text=_('Enter comma-separated tags.')
    )

    class Meta:
        model = Scammer
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': _('Description'), 'class': 'form-control', 'rows': 5}),
        }

class ScammerPhoneNumberForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        label=_('Scammer Phone Number'),
        required=False,
    )

    class Meta:
        model = ScammerPhoneNumber
        fields = ('phone_number',)

ScammerNameFormSet = inlineformset_factory(
    Scammer, ScammerName, fields=('name',), extra=1, can_delete=True,
    widgets={'name': forms.TextInput(attrs={'placeholder': _('Name'), 'class': 'form-control'})}
)

ScammerPhoneNumberFormSet = inlineformset_factory(
    Scammer, ScammerPhoneNumber, form=ScammerPhoneNumberForm, extra=1, can_delete=True
)

ScammerEmailFormSet = inlineformset_factory(
    Scammer, ScammerEmail, fields=('email',), extra=1, can_delete=True,
    widgets={'email': forms.EmailInput(attrs={'placeholder': _('Email'), 'class': 'form-control'})}
)

ScammerWebsiteFormSet = inlineformset_factory(
    Scammer, ScammerWebsite, fields=('website',), extra=1, can_delete=True,
    widgets={'website': forms.URLInput(attrs={'placeholder': _('Website'), 'class': 'form-control'})}
)

ScammerImageFormSet = inlineformset_factory(
    Scammer, ScammerImage, fields=('image',), extra=1, can_delete=True,
    widgets={'image': forms.ClearableFileInput(attrs={'class': 'form-control'})}
)

class ScammerPaymentAccountForm(forms.ModelForm):
    class Meta:
        model = ScammerPaymentAccount
        fields = ('account_number',)
        widgets = {
            'account_number': forms.TextInput(attrs={'placeholder': _('Payment Account: Number & Name'), 'class': 'form-control'})
        }

ScammerPaymentAccountFormSet = inlineformset_factory(
    Scammer, ScammerPaymentAccount, form=ScammerPaymentAccountForm, extra=1, can_delete=True
)

class ScammerCustomFieldForm(forms.ModelForm):
    class Meta:
        model = ScammerCustomField
        fields = ('field_label', 'field_value',)
        widgets = {
            'field_label': forms.TextInput(attrs={'placeholder': _('Custom Field Label'), 'class': 'form-control'}),
            'field_value': forms.TextInput(attrs={'placeholder': _('Custom Field Value'), 'class': 'form-control'}),
        }

ScammerCustomFieldFormSet = inlineformset_factory(
    Scammer, ScammerCustomField, form=ScammerCustomFieldForm, extra=1, can_delete=True
)

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = _('Required. Letters, digits and @/./+/-/_ only.')
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'username':
                field.widget.attrs.update({'placeholder': 'Username'})
            elif field_name == 'password':
                field.widget.attrs.update({'placeholder': 'Enter password'})
            elif field_name == 'password2':
                field.widget.attrs.update({'placeholder': 'Confirm password'})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Username')})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class ScammerProfileForm(forms.ModelForm):
    cases = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Enter Case IDs')}),
        help_text=_('Enter comma-separated case IDs.')
    )

    class Meta:
        model = ScammerProfile
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Profile Name')}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }