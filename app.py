from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from utils import put_and_delete, post, get

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(70))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(20))


class Offer(db.Model):
    __table_name__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Order(db.Model):
    __table_name__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(220))
    start_date = db.Column(db.String(70))
    end_date = db.Column(db.String(70))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


db.create_all()


@app.route('/users', methods=['GET', 'POST'])
def show_all_users():
    if request.method == 'POST':
        return post(User, db, request)
    result = get(db, User)
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def show_user_by_id(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        if request.method == 'GET':
            return jsonify({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            })
        return put_and_delete(user, request, db)
    return 'Такого юзера нет'


@app.route('/orders', methods=['GET', 'POST'])
def show_all_orders():
    if request.method == 'POST':
        return post(Order, db, request)
    result = get(db, Order)
    return jsonify(result)


@app.route('/orders/<int:order_id>')
def show_order_by_id(order_id):
    order = db.session.query(Order).filter(Order.id == order_id).first()
    if order:
        if request.method == 'GET':
            return jsonify({
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'address': order.address
            })
        return put_and_delete(order, request, db)
    return 'Такого заказа нет'


@app.route('/offers', methods=['GET', 'POST'])
def show_all_offers():
    if request.method == 'POST':
        return post(Offer, db, request)
    result = get(db, Offer)
    return jsonify(result)


@app.route('/offers/<int:offer_id>')
def show_offer_by_id(offer_id):
    offer = db.session.query(Offer).filter(Offer.id == offer_id).first()
    if offer:
        if request.method == 'GET':
            return jsonify({
                'id': offer.id,
                'order_id': offer.order_id,
                'executor_id': offer.executor_id
            })
        return put_and_delete(offer, request, db)
    return 'Такого предложения нет'


app.run()
