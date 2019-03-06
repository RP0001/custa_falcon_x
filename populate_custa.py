import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'custa_falcon_x.settings')

import django

django.setup()

# all the above steps are necessary for having the prerequisite django infrastructure
from custa.models import Base, Sauce, Top


def populate():
    bases = [
        {"name": "Macaroni", "price": 100}, ]

    for b in bases:
        add_base(b["name"], b["price"])
        print(b["name"] + " " + str(b["price"]))

    sauces = [
        {"name": "Macaroni Cheese", "price": 100, }, ]

    for s in sauces:
        add_sauce(s["name"], s["price"])
        print(s["name"] + " " + str(s["price"]))

    tops = [{"name": "Parmigiano Reggiano", "price": 50, }, ]

    for t in tops:
        add_top(t["name"], t["price"])
        print(t["name"] + " " + str(t["price"]))


def add_base(base, price=0):
    b = Base.objects.get_or_create(name=base, price=price)[0]
    b.save()
    return b


def add_sauce(sauce, price=0):
    s = Sauce.objects.get_or_create(name=sauce, price=price)[0]
    s.save()
    return s


def add_top(top, price=0):
    t = Top.objects.get_or_create(name=top, price=price)[0]
    t.save()
    return t


if __name__ == '__main__':
    print("Starting Custa population script...")
    populate()
