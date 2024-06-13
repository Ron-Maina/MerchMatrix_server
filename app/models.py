from .extensions import db
from flask_bcrypt import Bcrypt
# from sqlalchemy_serializer import SerializerMixin


from sqlalchemy.ext.hybrid import hybrid_property

bcrypt = Bcrypt()


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    number = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # _password_hash = db.Column(db.String, nullable = False)

    my_cart = db.relationship("Cart", backref = 'user')

    # @hybrid_property
    # def password_hash(self):
    #     return 'Unauthorized'
    
    # @password_hash.setter
    # def password_hash(self, password):
    #     password_hash = bcrypt.generate_password_hash(
    #         password.encode('utf-8')
    #     )
    #     self._password_hash = password_hash.decode('utf-8')

    # def authenticate(self, password):
    #     return bcrypt.check_password_hash(
    #         self._password_hash, password.encode('utf-8'))



class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_id = db.Column(db.Integer)
    payment_status = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_id': self.product_id,
            'payment_status': self.payment_status,
            'user_id': self.user_id
        }


