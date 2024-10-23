#!/usr/bin/env python3
import os
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, jsonify, request


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'restaurant_pizzas': [{
                'id': rp.id,
                'pizza': rp.pizza.to_dict(),
                'price': rp.price,
                'pizza_id': rp.pizza_id,
                'restaurant_id': rp.restaurant_id
            } for rp in restaurant.restaurant_pizzas]
        })
    return jsonify({"error": "Restaurant not found"}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    new_rp = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
    try:
        db.session.add(new_rp)
        db.session.commit()
        return jsonify({
            'id': new_rp.id,
            'pizza': new_rp.pizza.to_dict(),
            'price': new_rp.price,
            'pizza_id': new_rp.pizza_id,
            'restaurant': new_rp.restaurant.to_dict(),
            'restaurant_id': new_rp.restaurant_id
        }), 201
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
