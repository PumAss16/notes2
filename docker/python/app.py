from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Имитация базы данных (в реальности тут был бы PostgreSQL)
# Данные берутся из переменных окружения, которые мы зададим в Docker
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route('/')
def index():
    return f"Welcome to the API! Environment: {APP_ENV}, Version: {APP_VERSION}\n"

@app.route('/api/hello', methods=['GET'])
def hello():
    # Получаем имя из параметра URL: /api/hello?name=Иван
    name = request.args.get('name', 'Guest')
    return jsonify({
        "status": "success",
        "message": f"Hello, {name}!",
        "environment": APP_ENV
    })

if __name__ == '__main__':
    # Слушаем все интерфейсы на порту 5000
    app.run(host='0.0.0.0', port=5000)