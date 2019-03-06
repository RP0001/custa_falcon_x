import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'custa_falcon_x.settings')

import django

django.setup()

# all the above steps are necessary for having the prerequisite django infrastructure
from custa.models import Base, Sauce, Top


def populate():
    bases = [
        {"base": "Macaroni", "price": 100}, ]

    for b in bases:
        add_base(b["base"], b["price"])
        print(b["base"] + b["price"])

    sauces = [
        {"sauce": "Macaroni Cheese", "price": 100, }, ]

    for s in sauces:
        add_sauce(s["sauce"], s["price"])
        print(s["sauce"] + s["price"])

    tops = [{"top": "Parmigiano Reggiano", "price": 50, }, ]

    for t in tops:
        add_top(t["top"], t["price"])
        print(t["top"] + t["price"])


def add_base(base, price=0):
    b = Base.objects.get_or_create(base=base, price=price)[0]
    b.save()
    return b


def add_sauce(sauce, price=0):
    s = Sauce.objects.get_or_create(sauce=sauce, price=price)[0]
    s.save()
    return s


def add_top(top, price=0):
    t = Top.objects.get_or_create(top=top, price=price)[0]
    t.save()
    return t


if __name__ == '__main__':
    print("Starting Custa population script...")
    populate()
