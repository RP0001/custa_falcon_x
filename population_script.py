import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'custa_falcon_x.settings')

django.setup()

# all the above steps are necessary for having the prerequisite django infrastructure
from custa.models import Base, Sauce, Top, Custa


# populate all preset bases, sauces and tops as these will not change for the web app
def populate():
    bases = [
        {"name": "Fusilli (Wheat, Egg), contains ", "price": 100},
        {"name": "Spaghetti (Gluten Free, Rice, Dairy-Free)", "price": 170},
        {"name": "Fettuccine (Wheat, Egg)", "price": 170},
        {"name": "Linguine (Wheat, Egg)", "price": 180},
        {"name": "Penne (Wheat, Egg)", "price": 170},
        {"name": "Cannelloni (Wheat, Egg)", "price": 190},
        {"name": "Tagliatelle (Wheat, Egg)", "price": 140},
        {"name": "Farfalle (Wheat, Egg)", "price": 190},
        {"name": "Tortellini (Wheat, Egg)", "price": 130},
        {"name": "Macaroni (Gluten Free, Egg)", "price": 110},
        {"name": "Egg Noodles (Gluten Free)", "price": 130},
        {"name": "White Rice (Gluten Free)", "price": 180},
        {"name": "Brown Rice (Gluten Free)", "price": 180},
        {"name": "Basmati Rice (Gluten Free)", "price": 170},
        {"name": "Quinoa (Gluten Free)", "price": 290},
        {"name": "Amaranth (Gluten Free)", "price": 260},
        {"name": "Teff (Gluten Free)", "price": 220},
        {"name": "Buckwheat (Gluten Free)", "price": 280},
        {"name": "Mince Chicken Breast (Halal, Kosher)", "price": 320},
        {"name": "Mince Beef (Halal, Kosher)", "price": 400}]

    for b in bases:
        add_base(b["name"], b["price"])

    sauces = [
        {"name": "Ragu (Vegetarian, Gluten-Free)", "price": 370},
        {"name": "Bolognese (Halal, Kosher, Gluten Free)", "price": 220},
        {"name": "Pesto (Vegetarian, Gluten Free)", "price": 360},
        {"name": "Carbonara (Dairy, Egg)", "price": 470},
        {"name": "Puttanesca (Halal, Kosher, Gluten Free)", "price": 420},
        {"name": "Aglio e olio (Vegetarian, Gluten Free)", "price": 420},
        {"name": "Tomato Basil (Vegetarian, Gluten Free)", "price": 340},
        {"name": "Sockarooni (Gluten Free)", "price": 270},
        {"name": "Four Cheese Alfredo (Gluten-Free, Dairy)", "price": 480},
        {"name": "Mushroom sauce (Dairy, Egg)", "price": 280},
        {"name": "Creme fraiche with ham (Pork, Dairy)", "price": 400},
        {"name": "Aubergine and tomato (Gluten-Free)", "price": 270},
        {"name": "Cherry tomato and mozarella (Gluten-Free, Dairy)", "price": 440},
        {"name": "Macaroni Cheese (Dairy)	", "price": 500},
        {"name": "Tikka Masala (Halal, Kosher, Chicken, Low-Carb)", "price": 280},
        {"name": "Bacon Cream  (Pork, Dairy, Egg)", "price": 310},
        {"name": "Chicken Sweet & Sour (Halal, Kosher, Gluten-Free)", "price": 390},
        {"name": "Puff Candy Cream (Dairy-Free, Sugar)", "price": 360},
        {"name": "Cheese Cake (Dessert, Dairy, Sugar)", "price": 400},
        {"name": "Ricotta and Blueberry (Dessert, Dairy, Sugar)", "price": 330}
    ]

    for s in sauces:
        add_sauce(s["name"], s["price"])

    tops = [{"name": "Bacon", "price": 190},
            {"name": "Prawn (Halal, Kosher)", "price": 300},
            {"name": "Parmiggiano Regiano (Dairy)", "price": 240},
            {"name": "Grana Padano (Dairy)", "price": 270},
            {"name": "Pecorino Romano (Dairy)", "price": 190},
            {"name": "Peanut Butter Sauce (Peanuts)", "price": 260},
            {"name": "Pork Scratchings (Pork)", "price": 100},
            {"name": "Cream (Dairy)", "price": 200},
            {"name": "Tofu (Vegetarian)", "price": 120},
            {"name": "Double Sauce (doubles chosen sauce)", "price": 100},
            {"name": "Chilli Flakes (Vegetarian)", "price": 160},
            {"name": "Ruccola (Vegetarian)", "price": 160},
            {"name": "Chopped Tomatoes (Vegetarian)", "price": 290},
            {"name": "Chopped Onions (Vegetarian)", "price": 180},
            {"name": "Lemon Sauce (Vegetarian)", "price": 150},
            {"name": "Kimchi (Vegetarian)", "price": 230},
            {"name": "Nutella", "price": 140},
            {"name": "Fig Jam (Sugar)", "price": 110},
            {"name": "Blueberry Jam (Sugar)", "price": 220},
            {"name": "Strawberry Jam (Sugar)", "price": 160}
            ]

    for t in tops:
        add_top(t["name"], t["price"])

    # create user 0 first for pre-set custas
    my_custom_sql()

    # preset custas are created here, this is enough since other custas are created by user and
    # therefore are user-private
    custas = [
        {"name": "PRESET - Gluten Free Mac&Cheese", "price": 300, "base_id": 10, "sauce_id": 14, "top_id": 3},
        {"name": "PRESET - Halal / Kosher Chicken Tikka Masala", "price": 400, "base_id": 14, "sauce_id": 15,
         "top_id": 11},
        {"name": "PRESET - Halal Bolognese", "price": 350, "base_id": 7, "sauce_id": 2, "top_id": 3},
        {"name": "PRESET - Cheesecake", "price": 250, "base_id": 10, "sauce_id": 19, "top_id": 19},
        {"name": "PRESET - Vegetarian Classic Pasta", "price": 350, "base_id": 1, "sauce_id": 1, "top_id": 4}
    ]

    for c in custas:
        add_custa(c["name"], c["price"], c["base_id"], c["sauce_id"], c["top_id"], 0)


# customised method for adding all ingredient details
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


# customised method generating DDL SQL necessary for creating user 0
# user 0 is an admin user with sole responsibility of owning the preset custas in the web app
def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute(
            """
        insert into auth_user values (0,
                       "pbkdf2_sha256$36000$3CEeA3Z3FPGA$n4ygtRNKfIhY8sVdmJerW75ks+ytGi0LlIq9CfBosJw=",
                       current_date,
                         TRUE	,
                         "alpha",
                         "beta"	,
                         "user@user.user",
                         FALSE	,
                         TRUE	,
                         CURRENT_date,
                         "user0")
            """
        )


# customised method for adding all custa details
def add_custa(name, price, base_id, sauce_id, top_id, user_id=0):
    c = Custa.objects.get_or_create(name=name, price=price, base_id=base_id, sauce_id=sauce_id, top_id=top_id,
                                    user_id=user_id)[0]
    c.save()
    return c


# main method
if __name__ == '__main__':
    print("Starting Custa population script...")
    populate()
