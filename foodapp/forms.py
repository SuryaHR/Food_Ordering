from django import forms
from .models import CustomUser

from django import forms
from foodapp.models import CustomUser, Restaurant

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'contact', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please try again.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.set_password(password)  # Set and hash the password
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_image']
