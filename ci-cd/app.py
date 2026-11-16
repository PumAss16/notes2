from flask import Flask, jsonify, request

app = Flask(__name__)

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("На ноль делить нельзя!")
    return a / b

@app.route('/api/add')
def api_add():
    a = int(request.args.get('a', 0))
    b = int(request.args.get('b', 0))
    return jsonify({"result": add(a, b)})

@app.route('/api/divide')
def api_divide():
    a = int(request.args.get('a', 0))
    b = int(request.args.get('b', 1))
    try:
        result = divide(a, b)
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)