from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Stock, UserStock
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_pyfile('config.py')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    session = Session()

    # Check if the username already exists
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        session.close()
        return jsonify({'error': 'Username already exists'}), 400

    # Create a new user and add it to the session
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()

    created_user = session.query(User).filter_by(username=username).first()
    created_user_id = created_user.id

    # Close the session
    session.close()

    return jsonify({'user_id': created_user_id}), 201



@app.route('/login', methods=['POST'])
def login():
    """
    Log in existing user.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    session = Session()
    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'user_id': user.id}), 200


@app.route('/all-stocks', methods=['GET'])
def all_stocks():
    """
    Retrieve all available stocks.
    """
    session = Session()
    stocks = session.query(Stock).order_by(Stock.quantity.desc()).all()
    session.close()

    stock_list = [{'id': stock.id, 'name': stock.name, 'price': stock.price, 'quantity': stock.quantity} for stock in
                  stocks]
    return jsonify(stock_list), 200


@app.route('/user-stocks/<int:user_id>', methods=['GET'])
def user_stocks(user_id):
    """
    Retrieve all user owned stocks.
    """
    session = Session()
    user = session.query(User).get(user_id)

    if not user:
        session.close()
        return jsonify({'error': 'User not found'}), 404

    user_stocks = [{'stock_id': stock.stock_id, 'name': stock.stock.name, 'price': stock.stock.price,
                    'bought_quantity': stock.bought_quantity} for stock in user.stocks if stock.bought_quantity > 0]
    session.close()

    return jsonify(user_stocks), 200


@app.route('/buy-stock', methods=['POST'])
def buy_stock():
    """
    Buy a certain quantity of a stock by a user.
    """
    data = request.json
    user_id = data.get('user_id')
    stock_id = data.get('stock_id')
    quantity = data.get('quantity')

    # Check if all required fields are present in the request
    if not user_id or not stock_id or not quantity:
        return jsonify({'error': 'User ID, stock ID, and quantity are required'}), 400

    session = Session()
    user = session.query(User).get(user_id)
    stock = session.query(Stock).get(stock_id)

    # Check if the user and stock exist in the database
    if not user or not stock:
        session.close()
        return jsonify({'error': 'User or stock not found'}), 404

    # Check if there are enough stocks available to buy
    if stock.quantity < quantity:
        session.close()
        return jsonify({'error': 'Not enough stocks available to buy'}), 400

    # Check if quantity is positive
    if quantity <= 0:
        session.close()
        return jsonify({'error': 'You can not buy this amount'}), 400

    # Check if the user has sufficient balance to make the purchase
    total_cost = stock.price * quantity
    if user.balance < total_cost:
        session.close()
        return jsonify({'error': 'Insufficient balance'}), 400

    user.balance -= total_cost

    existing_user_stock = session.query(UserStock).filter_by(user_id=user_id, stock_id=stock_id).first()

    # Update existing user stock quantity or create a new entry
    if existing_user_stock:
        existing_user_stock.bought_quantity += quantity
    else:
        user_stock = UserStock(user_id=user_id, stock_id=stock_id, bought_quantity=quantity)
        session.add(user_stock)

    stock.quantity -= quantity

    session.commit()
    session.close()

    return jsonify({'message': 'Stock bought successfully'}), 200

@app.route('/sell-stock', methods=['POST'])
def sell_stock():
    """
    Sell a certain quantity of a stock by a user.
    """
    data = request.json
    user_id = data.get('user_id')
    stock_id = data.get('stock_id')
    quantity = data.get('quantity')

    # Check if all required fields are present in the request
    if not user_id or not stock_id or not quantity:
        return jsonify({'error': 'User ID, stock ID, and quantity are required'}), 400

    session = Session()

    user = session.query(User).get(user_id)
    stock = session.query(Stock).get(stock_id)

    # Check if the user and stock exist in the database
    if not user or not stock:
        session.close()
        return jsonify({'error': 'User or stock not found'}), 404

    user_stock = session.query(UserStock).filter_by(user_id=user_id, stock_id=stock_id).first()

    # Check if quantity is positive
    if quantity <= 0:
        session.close()
        return jsonify({'error': 'You can not sell this amount'}), 400

    # Check if the user has enough stocks to sell
    if not user_stock or user_stock.bought_quantity < quantity:
        session.close()
        return jsonify({'error': 'Insufficient stocks to sell'}), 400

    total_price = stock.price * quantity
    user.balance += total_price
    user_stock.bought_quantity -= quantity
    stock.quantity += quantity

    session.commit()
    session.close()

    return jsonify({'message': 'Stock sold successfully'}), 200

@app.route('/add-stock', methods=['POST'])
def add_stock():
    """
    Add a new stock to the database.
    """
    data = request.json
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')

    if not name or not price or not quantity:
        return jsonify({'error': 'Name, price, and quantity are required'}), 400

    session = Session()
    stock = Stock(name=name, price=price, quantity=quantity)
    session.add(stock)
    session.commit()
    session.close()

    return jsonify({'message': 'Stock added successfully'}), 201

@app.route('/user-info/<int:user_id>', methods=['GET'])
def user_info(user_id):
    """
    Retrieve user information by user ID.
    """
    session = Session()
    user = session.query(User).get(user_id)

    if not user:
        session.close()
        return jsonify({'error': 'User not found'}), 404

    session.close()

    return jsonify({'user_id': user.id, "username":user.username, "balance": user.balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
