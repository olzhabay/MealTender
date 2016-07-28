from django import forms
from app.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, label='Username')
    email = forms.EmailField(widget=forms.TextInput, label='Email')
    first_name = forms.CharField(widget=forms.TextInput, label='First Name')
    last_name = forms.CharField(widget=forms.TextInput, label='Last Name')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password(again)')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords does not match")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.create_user(self.username, self.email, self.cleaned_data['password1'])
        user.first_name = self.first_name
        user.last_name = self.username
        if commit:
            user.save()
        return user
