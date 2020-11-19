from django import forms
from django.utils import timezone

from .models import Purchase,Genre,Siteuser,NameOnlyUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UsernameField
from django.utils.text import capfirst


UserModel = get_user_model()

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['name','genre','price','purchase_date']
        labels = {
            'name':'名前',
            'genre':'ジャンル',
            'price':'価格',
            'purchase_date':'購入日',
        }
        widgets = {
            'purchase_date': forms.SelectDateWidget(years=[x for x in range(timezone.now().year - 1,timezone.now().year + 1)]),
        }
        label_suffix = ''

class SiteuserForm(forms.ModelForm):
    class Meta:
        model = Siteuser
        fields = ['monthly_budget']
        labels = {
        'monthly_budget':'今月の予算',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name',]
        labels = {
            'genre_name':"ジャンル名"
        }



class AuthenticationFormWithoutPassword(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))


    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args,label_suffix="",**kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')

        if username is not None:
            self.user_cache = authenticate(self.request, username=username)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

class SignUpForm(forms.ModelForm):
    class Meta:
        model = NameOnlyUser
        fields = ['username']
