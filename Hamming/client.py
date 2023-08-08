
from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

def calcRedundantBits(m):
    for i in range(m):
        if(2**i >= m + i + 1):
            return i
#SE INTRODUCE EL RUIDO
 def introduceErrors(hamming_code):
    # Elige dos posiciones aleatorias en la trama para cambiar sus valores
    num_bits = len(hamming_code)
    error_positions = random.sample(range(num_bits), 2)

    # Cambia el valor de los bits en las posiciones seleccionadas
    for pos in error_positions:
        hamming_code = hamming_code[:pos] + ('0' if hamming_code[pos] == '1' else '1') + hamming_code[pos + 1:]

    return hamming_code
 
def posRedundantBits(data, r):
    j = 0
    k = 1
    m = len(data)
    res = ''
 
    for i in range(1, m + r+1):
        if(i == 2**j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
 
    return res[::-1]
 
 
def calcParityBits(arr, r):
    n = len(arr)
 
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
 
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
    return arr


def generateHammingCode(data):
    # Step 1: Solicitar una trama en binario
    # La información original es 'data'
 
    # Step 2: Calcular la información adicional (bits redundantes)
    m = len(data)
    r = calcRedundantBits(m)
 
    # Step 3: Concatenar la información original con los bits redundantes
    arr = posRedundantBits(data, r)
    arr = calcParityBits(arr, r)

    return arr


@socketio.on('connect')
def test_connect():
    data_input = input("Ingrese una trama en binario: ")
    hamming_code = generateHammingCode(data_input)
    send(hamming_code)

if __name__ == '__main__':
    socketio.run(app, host='192.168.1.33', port=4000)
