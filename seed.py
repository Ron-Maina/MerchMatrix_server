from app.models import Users, Cart
from app.extensions import db
from app import create_app
from random import randint


app = create_app()

with app.app_context():
    Users.query.delete()
    Cart.query.delete()

    email_list = [
        "me@gmail.com",
        "you@gmail.com",
        "us@gmail.com"
    ]

    roles = ['admin', 'customer']

    user_list = []
    for email in email_list:
        for role in roles:
            user = Users(
                name = "Me",
                number = randint(1, 150),
                email = email,
                role = role
            )
            if role == 'admin':
                roles.remove(role)
        user_list.append(user)

    db.session.add_all(user_list)
    db.session.commit()
    print("SEEDED USERS...")


    pizza_list = [
    "Margherita Pizza",
    "Pepperoni Pizza",
    "Hawaiian Pizza",
    "Vegetarian Pizza",
    "Supreme Pizza",
    "BBQ Chicken Pizza",
    "Mushroom Pizza",
    "Sausage and Pepper Pizza",
    "Buffalo Chicken Pizza",
    "Meat Lover's Pizza",
    "Four Cheese Pizza",
    "Pesto Chicken Pizza",
    "Spinach and Feta Pizza",
    "White Pizza",
    "Artichoke and Olive Pizza",
    "Bacon and Egg Pizza",
    "Veggie Delight Pizza",
    "Taco Pizza",
    "Chicken Alfredo Pizza",
    "Pineapple and Ham Pizza",
    "Greek Pizza",
    "Tomato and Basil Pizza",
    "Chicken and Broccoli Pizza",
    "Sausage and Mushroom Pizza",
    "Prosciutto and Arugula Pizza",
    "BBQ Pulled Pork Pizza",
    "Buffalo Cauliflower Pizza",
    "Anchovy and Olive Pizza",
    "Shrimp Scampi Pizza",
    "Truffle Mushroom Pizza",
    "Fig and Prosciutto Pizza",
    "Clam and Garlic Pizza",
    "Pesto Veggie Pizza",
    "Roasted Red Pepper Pizza",
    "Buffalo Ranch Chicken Pizza",
    "BBQ Beef Brisket Pizza",
    "Salami and Pepperoncini Pizza",
    "Caramelized Onion and Gorgonzola Pizza",
    "Caprese Pizza",
    "Sun-Dried Tomato and Pesto Pizza",
    "Pulled BBQ Jackfruit Pizza",
    "Margherita with Burrata Pizza",
    "Bacon Ranch Chicken Pizza",
    "Steak and Blue Cheese Pizza",
    "Sausage and Ricotta Pizza",
    "Tandoori Chicken Pizza",
    "Mexican Fiesta Pizza",
    "Pumpkin and Sage Pizza",
    "Garlic Knot Crust Pizza"
    ]

    pizzas = []
    for pizza_name in pizza_list:

        cart = Cart(
            product_name = pizza_name,
            product_id = randint(1, 150),
            user_id = randint(1,3)
        )
        pizzas.append(cart)

    db.session.add_all(pizzas)
    db.session.commit()
    print('SEEDED CART....')