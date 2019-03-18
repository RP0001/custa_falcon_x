from django import forms
from django.contrib.auth.models import User
from django.forms import RadioSelect

from custa.models import UserProfile, Custa, Order, Requirement


# this is the form used to register
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# extra information that is used by the user to register such as phone or address
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('pref_name', 'phone', 'address')


# form used to create new custas
class CustaForm(forms.ModelForm):
    class Meta:
        model = Custa
        fields = ('name', 'price', 'base', 'sauce', 'top')
        widgets = {
            'base': RadioSelect,
            'sauce': RadioSelect,
            'top': RadioSelect,
        }


# form used to create order, only contains is_delivery
# and total fields since everything else is managed in views
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('is_delivery', 'total')


# form used by user to submit requirement/request for the company
class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ('description',)
