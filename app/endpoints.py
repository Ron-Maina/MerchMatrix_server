from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token, 
                                jwt_required, get_jwt,
                                current_user, get_jwt_identity)
from werkzeug.exceptions import BadRequest
from random import randint


from .extensions import db
from .api_models import users_model, cart_model, user_login_model, user_registration_model
from .models import Users, Cart

ns = Namespace("merchmatrixapi")


@ns.route('/users')
class UsersAPI(Resource):
    @ns.marshal_list_with(users_model)
    def get(self):
        return Users.query.all()
    


@ns.route('/signup')
class SignUp(Resource):
    @ns.expect(user_registration_model)
    def post(self):
        try:
            data = request.get_json()
            user_data = data.get('user', {})

            # subject = data.get('sub')
            
            existing_user = Users.query.filter_by(email=data.get('email')).first()

            if existing_user:
                return jsonify({'message': 'Email already exists'}, 403)
            
            # if subject:
            #     new_user = Users(
            #         username = data.get('given_name'),
            #         email = data.get('email'),
            #     )
            #     db.session.add(new_user)
            #     db.session.commit()
            else:
                new_user = Users(
                    name = user_data.get('username'),
                    email = user_data.get('email'),
                    number = user_data.get('number'),
                    role = 'customer',
                )
                new_user.password_hash = user_data.get('password')

                db.session.add(new_user)
                db.session.commit()


            user_dict = {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "number": new_user.number,
            }

            result = make_response(
                jsonify(user_dict),
                200
            )
            return result
        
        except ValueError:
            raise BadRequest(["validation errors"])  
    


@ns.route('/login')
class Login(Resource):
    @ns.expect(user_login_model) 
    def post(self):
        try:
            data = request.get_json()
            user_data = data.get('user', {})
            # subject = data.get('sub')

            user = Users.query.filter_by(email = user_data.get('email')).first()
            password = user_data.get('password')

            # if subject:
            #     access_token = create_access_token(identity=data.get('email'))
            #     refresh_token = create_refresh_token(identity=data.get('email'))

            #     response = make_response(jsonify(
            #         {
            #             "username": data.get('name'),
            #             "access_token": access_token, 
            #             "refresh_token": refresh_token, 
            #             "id": user.id,  
            #         },
            #         201
            #     ))
            #     response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True)

            #     return response
               
            if (user) and (user.authenticate(password) == True):
                access_token = create_access_token(identity=user.email)
                refresh_token = create_refresh_token(identity=user.email)

                user_dict = {
                        "username": user.name,
                        "cart": [cart_item.to_dict() for cart_item in user.my_cart],
                        "tokens": {
                            "access": access_token,
                            "refresh": refresh_token, 
                        },
                        "id": user.id,  
                }

                response = make_response(
                    jsonify(user_dict),
                    200
                )
                return response
            
            return jsonify ({"error": "Invalid Username or Password"}), 400

        except ValueError:
            raise BadRequest(["validation errors"])  
        

@ns.route('/refresh')
class RefreshSession(Resource):
    @jwt_required(refresh=True)
    def get(self):
        try:
            identity = get_jwt_identity()
            user = Users.query.filter_by(email = identity).first()

            if not user:
                raise ValueError("User not found")

            new_access_token = create_access_token(identity=identity)
            # new_refresh_token = create_refresh_token(identity=identity)


            user_dict = {
                "username": user.name,
                "cart": [cart_item.to_dict() for cart_item in user.my_cart],
                "tokens": {
                    "access": new_access_token,
                },
                "id": user.id,  
            }

            response = make_response(
                jsonify(user_dict),
                200
            )
            return response
    
        except ValueError:
            raise BadRequest(["validation errors"]) 

        
    
@ns.route('/addtocart')
class AddToCart(Resource):
    @jwt_required()
    @ns.expect(cart_model)
    def post(self):
        try:
            data = request.get_json()
            product_data = data.get('product', {})

            print(data)

            if data:
                added_to_cart = Cart(
                    product_name = product_data.get('title'),
                    product_id = product_data.get('product_id'),
                    price = product_data.get('price'),
                    payment_status = product_data.get(False),
                    user_id = product_data.get("user_id"),
                )

                db.session.add(added_to_cart)
                db.session.commit()

                response = make_response(
                    jsonify(added_to_cart.to_dict()),
                    200
                )
                return response

        except ValueError:
            raise BadRequest(["validation errors"])  


@ns.route('/mycart')
class AddToCart(Resource):
    @jwt_required()
    def get(self):
        try: 
            identity = get_jwt_identity()
            user = Users.query.filter_by(email=identity).first()

            if not user:
                return make_response(jsonify({"error": "User not found"}), 404)

            # Serialize the Cart objects
            cart_items = [cart_item.to_dict() for cart_item in user.my_cart]

            response = make_response(
                jsonify(cart_items),
                200
            )
            return response

        except ValueError:
            raise BadRequest(["validation errors"])



