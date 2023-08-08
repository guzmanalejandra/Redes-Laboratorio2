# archivo: server.py
import random
from flask import Flask, request
from flask_socketio import SocketIO
import json


app = Flask(__name__)
socketio = SocketIO(app)

def introduce_noise(data):
    # Convert the string to a list so we can modify it
    data_list = list(data)

    # Choose a random index
    index = random.randint(0, len(data_list) - 1)

    # Flip the bit at the chosen index
    if data_list[index] == '0':
        data_list[index] = '1'
    else:
        data_list[index] = '0'

    # Convert the list back to a string
    noisy_data = ''.join(data_list)

    return noisy_data

def fletcher16(data):
    sum1 = 0xff
    sum2 = 0xff

    # Split the data by spaces to get each 8-bit chunk
    data_chunks = data.split(" ")

    for chunk in data_chunks:
        sum1 += int(chunk, 2)
        sum2 += sum1

        sum1 = (sum1 & 0xff) + (sum1 >> 8)
        sum2 = (sum2 & 0xff) + (sum2 >> 8)

    # Second reduction step to reduce sums to 8 bits
    sum1 = (sum1 & 0xff) + (sum1 >> 8)
    sum2 = (sum2 & 0xff) + (sum2 >> 8)

    return (sum2 << 8) | sum1



def binary_to_string(binary):
    return ''.join([chr(int(b, 2)) for b in binary.split(' ')])

@socketio.on('connect')
def handle_connect():
    print('Un cliente se ha conectado')

@socketio.on('mensaje_python')
def handle_mensaje_python(msg):
    JsonObj = json.loads(msg)
    binary = JsonObj['message']

    if binary_to_string(binary) == "show_error":
        print("Error en el mensaje")
        binary = introduce_noise(binary)

    fletcheckSum = JsonObj['fletCheck']
    checkSum = fletcher16(binary)

    
    if checkSum == fletcheckSum:
        emit = f"Mensaje recibido: , {binary}\nChecksum recibido: , {fletcheckSum}\nChecksum calculado: , {checkSum}\nMensaje correcto\nMensaje en ASCII:{binary_to_string(binary)}", 
        print(emit)
    else:
        emit = f"Mensaje recibido: , {binary}\nChecksum recibido: , {fletcheckSum}\nChecksum calculado: , {checkSum}\nMensaje incorrecto\nMensaje en ASCII:{binary_to_string(binary)}"
        print(emit)
    # Retransmitir el mensaje a todos los clientes excepto al emisor
    socketio.emit('mensaje_servidor', emit, skip_sid=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('El cliente se ha desconectado')

if __name__ == '__main__':
    print('Servidor corriendo en *:3000')
    socketio.run(app, host='0.0.0.0', port=3000)