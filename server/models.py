from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

  
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    

    #serialization rules
    def to_dict(self):
        return {
        "id": self.id,
        "name":self.name,
        "address": self.address
        
        }

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')


    #  serialization rules
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "ingredients": self.ingredients
            
            
        }

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # add relationships
pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

    #serialization rules
def to_dict(self):
    return {
        "id":self.id
    }
    # validation
@validates('price')
def validate_strength(self, key, price):
        if not (1000 <= price <= 5000):
            raise ValueError("Price must be between 1000 and 5000.")
        return price
def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
