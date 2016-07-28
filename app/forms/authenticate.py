from django import forms
from django.contrib.auth import authenticate, login


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def authenticate(self, request):
        user = authenticate(username=self.username, password=self.password)
        if user is not None:
            if not user.is_active:
                raise forms.FieldError("Account have been disabled")
            else:
                login(request, user)
        else:
            raise forms.FieldError("Username and password were incorrect")

    class Meta:
        fields = ['username', 'password']
