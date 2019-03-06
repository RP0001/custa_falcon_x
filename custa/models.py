from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

char_field_max_length = 128


class Base(models.Model):
    # id primary key is by default
    base = models.CharField(max_length=char_field_max_length, unique=True) # Unique base.
    price = models.IntegerField(default=0) # Remember price is in pence henceforth!

    def __str__(self):
        return self.base


class Sauce(models.Model):
    # id primary key is by default
    sauce = models.CharField(max_length=char_field_max_length, unique=True)  # Unique sauce.
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.sauce


class Top(models.Model):
    # id primary key is by default
    top = models.CharField(max_length=char_field_max_length, unique=True)  # Unique top.
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.top


class Custa(models.Model):
    # id primary key is by default
    name = models.CharField(max_length=char_field_max_length, unique=True)
    price = models.IntegerField(default=0)
    base_id = models.OneToOneField(Base, on_delete=models.CASCADE)
    sauce_id = models.OneToOneField(Sauce, on_delete=models.CASCADE)
    top_id = models.OneToOneField(Top, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# User is built in and has username, email, password, first_name and last_name. UserProfile extends user.
class UserProfile(models.Model):
    # id primary key is by default
    user = models.OneToOneField(User)
    pref_name = models.CharField(max_length=char_field_max_length, null=True)  # Not necessary to have a preferred name.
    phone = models.IntegerField(null=False) # Must provide a phone number
    address = models.CharField(max_length=char_field_max_length, null=False) # Must provide an address.

    def __str__(self):
        return self.user.username


class Order(models.Model):
    # id primary key is by default
    date = models.DateField(null=False) # Must provide Date Field.
    order_details = models.CharField(max_length=char_field_max_length, null=False) # Must provide order details.
    username = models.ForeignKey(User, on_delete=models.CASCADE)



