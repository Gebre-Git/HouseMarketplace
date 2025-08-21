from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class SellerSignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Name", max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "email", "phone_number")  # password fields come from UserCreationForm

    def save(self, commit=True):
        user = super().save(commit=False)
        # map Name -> first_name field
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class BuyerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')    
