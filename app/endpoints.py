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
                    name = data.get('username'),
                    email = data.get('email'),
                    number = data.get('number'),
                    role = 'customer',
                )
                # new_user.password_hash = data.get('password')

                db.session.add(new_user)
                db.session.commit()


            return jsonify(new_user.to_dict(), 201)
        
        except ValueError:
            raise BadRequest(["validation errors"])  
    


@ns.route('/login')
class Login(Resource):
    @ns.expect(user_login_model)
    def post(self):
        try:
            print('server reached')
            data = request.get_json()
            # subject = data.get('sub')

            user = Users.query.filter_by(email = data.get('email')).first()
            # password = data.get('password')

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
               
            if (user):
                access_token = create_access_token(identity=user.email)
                refresh_token = create_refresh_token(identity=user.email)

                response = make_response(jsonify(
                    {
                        "username": user.name,
                        "cart": [cart_item.to_dict() for cart_item in user.my_cart],
                        "tokens": {
                            "access": access_token,
                            "refresh": refresh_token, 
                        },
                        "id": user.id,  
                    },
                    200
                ))
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            
            return jsonify ({"error": "Invalid Username or Password"}), 400

        except ValueError:
            raise BadRequest(["validation errors"])  
        

@ns.route('/refresh')
class RefreshSession(Resource):
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)

        return make_response(
            jsonify({"access_token": new_access_token}),
            200
        )
    

@ns.route('/addtocart')
class AddToCart(Resource):
    @ns.expect(cart_model)
    def post(self):
        try:
            data = request.get_json()

            print(data)

            if data:
                added_to_cart = Cart(
                    product_name = data.get('title'),
                    product_id = data.get('id'),
                    payment_status = data.get(False),
                    user_id = randint(1,10),
                )

                db.session.add(added_to_cart)
                db.session.commit()

        except ValueError:
            raise BadRequest(["validation errors"])  




# 'id': self.id,
#             'product_name': self.product_name,
#             'product_id': self.product_id,
#             'payment_status': self.payment_status,
#             'user_id': self.user_id

