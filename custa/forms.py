from django import forms
from django.contrib.auth.models import User
from django.forms import RadioSelect, TextInput

from custa.models import UserProfile, Custa, Order, OrderCusta


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('pref_name', 'phone', 'address')


class CustaForm(forms.ModelForm):
    class Meta:
        model = Custa
        fields = ('name', 'price', 'base', 'sauce', 'top')
        widgets = {
            'base': RadioSelect,
            'sauce': RadioSelect,
            'top': RadioSelect,
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('is_delivery', 'total')


# class OrderCustaForm(forms.ModelForm):
#     clas