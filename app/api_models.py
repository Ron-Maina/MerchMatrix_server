from .extensions import api
from flask_restx import fields

user_registration_model = api.model("Signup", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
})

user_login_model = api.model("Login", {
    "email": fields.String,
    "password": fields.String,
})

cart_model = api.model("Cart", {
    "product_name":fields.String,
    "product_id": fields.Integer,
    # "payment_status": fields.Boolean,
})


users_model = api.model("Users", {
    "id": fields.Integer,
    "name":fields.String,
    "number": fields.String,
    "email": fields.String,
    "my_cart": fields.Nested(cart_model)
})

