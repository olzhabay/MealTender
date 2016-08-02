from app.models import Profile, Address
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'zip_code', 'city', 'country')
