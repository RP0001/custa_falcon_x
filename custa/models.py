from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

char_field_max_length = 128


class Sauce(models.Model):
    # id primary key is by default
    name = models.CharField(max_length=char_field_max_length, unique=True)  # Unique sauce.
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Top(models.Model):
    # id primary key is by default
    name = models.CharField(max_length=char_field_max_length, unique=True)  # Unique top.
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Base(models.Model):
    # id primary key is by default
    name = models.CharField(max_length=char_field_max_length, unique=True)  # Unique base.
    price = models.IntegerField(default=0)  # Remember price is in pence henceforth!

    def __str__(self):
        return self.name


class Custa(models.Model):
    # id primary key is by default
    name = models.CharField(max_length=char_field_max_length, unique=True)
    price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    base = models.ForeignKey(Base, on_delete=models.CASCADE, unique=False)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE, unique=False)
    top = models.ForeignKey(Top, on_delete=models.CASCADE, unique=False)

    def __str__(self):
        return self.name


# User is built in and has username, email, password, first_name and last_name. UserProfile extends user.
class UserProfile(models.Model):
    # id primary key is by default
    user = models.OneToOneField(User)
    pref_name = models.CharField(max_length=char_field_max_length, null=True)  # Not necessary to have a preferred name.
    phone = models.IntegerField(null=False)  # Must provide a phone number
    address = models.CharField(max_length=char_field_max_length, null=False)  # Must provide an address.

    def __str__(self):
        return self.user.username


class Order(models.Model):
    # id primary key is by default
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(auto_now_add=True, null=True)
    is_delivery = models.BooleanField(default=False)
    total = models.IntegerField(default=0, null=False)


class OrderCusta(models.Model):
    # id primary key is by default
    order = models.ForeignKey(Order, on_delete=models.CASCADE, unique=False)
    custa = models.ForeignKey(Custa, on_delete=models.CASCADE, unique=False)
    quantity = models.IntegerField(null=False)  # Must provide a quantity
