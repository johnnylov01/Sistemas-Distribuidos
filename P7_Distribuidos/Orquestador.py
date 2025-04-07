from flask import Flask, request, jsonify
import requests
app=Flask(__name__)
#Mapa de microservicios y sus rutas
microservicios = {
    "sumar": "http://localhost:5001/suma",
    "restar": "http://localhost:5002/resta",
    "multiplicar": "http://localhost:5003/multiplicacion",
    "dividir": "http://localhost:5004/division"
}
@app.route('/calcular', methods=['GET'])
def calculo():
    operacion=request.args.get('op')
    a=request.args.get('a')
    b=request.args.get('b')
    if operacion not in microservicios:
        return jsonify({'error':'Operacion no valida o inexistente'}),400
    try:
        respuesta=requests.get(microservicios[operacion], params={'a':a,'b':b})
        return jsonify(respuesta.json()), respuesta.status_code
    except request.exceptions.ConnectionError:
        return jsonify({'error':'Error de conexion con el microservicio'}), 500
if __name__=='__main__':
    app.run(port=5000)
        
