from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/division', methods=['GET'])
def sumar():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    if b == 0:
        return jsonify({'error': 'División por cero no permitida'}), 400
    else:
        return jsonify({'resultado': a / b})

if __name__ == '__main__':
    app.run(port=5004)
