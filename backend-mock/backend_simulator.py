from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Предположим, что пользователь зарегистрирован успешно
    # и вернем имитированный идентификатор пользователя
    return jsonify({'user_id': 1}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Предположим, что пользователь успешно вошел в систему
    # и вернем имитированный идентификатор пользователя
    return jsonify({'user_id': 1}), 200


@app.route('/all-stocks', methods=['GET'])
def all_stocks():
    # Предположим, что есть несколько акций в базе данных
    stocks = [
        {'id': 1, 'name': 'Apple', 'price': 150.0, 'quantity': 100},
        {'id': 2, 'name': 'Google', 'price': 250.0, 'quantity': 200},
        {'id': 3, 'name': 'Microsoft', 'price': 100.0, 'quantity': 150}
    ]
    return jsonify(stocks), 200


@app.route('/user-stocks/<int:user_id>', methods=['GET'])
def user_stocks(user_id):
    # Предположим, что у пользователя есть некоторые акции
    user_stocks = [
        {'stock_id': 1, 'name': 'Apple', 'price': 150.0, 'bought_quantity': 10},
        {'stock_id': 2, 'name': 'Google', 'price': 250.0, 'bought_quantity': 5}
    ]
    return jsonify(user_stocks), 200


@app.route('/buy-stock', methods=['POST'])
def buy_stock():
    # Предположим, что акция успешно куплена
    return jsonify({'message': 'Stock bought successfully'}), 200


@app.route('/sell-stock', methods=['POST'])
def sell_stock():
    # Предположим, что акция успешно продана
    return jsonify({'message': 'Stock sold successfully'}), 200


@app.route('/user-info/<int:user_id>', methods=['GET'])
def user_info(user_id):
    # Предположим, что у нас есть информация о пользователе
    user_info = {'user_id': user_id, 'username': 'JohnDoe', 'balance': 10000.0}
    return jsonify(user_info), 200


if __name__ == '__main__':
    app.run(debug=True)
