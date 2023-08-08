// Fletcher
function stringToBinary(input) {
    return input.split('').map(function(char) {
        return char.charCodeAt(0).toString(2).padStart(8, '0');
    }).join(' ');
}
    
function binaryToString(binary) {
        return binary.split(' ').map(function(bin) {
            return String.fromCharCode(parseInt(bin, 2));
        }).join('');
}
    
function fletcher16(data) {
    let sum1 = 0xff;
    let sum2 = 0xff;

    // Split the data by spaces to get each 8-bit chunk
    let dataChunks = data.split(" ");

    for (let i = 0; i < dataChunks.length; i++) {
        sum1 += parseInt(dataChunks[i], 2);
        sum2 += sum1;

        sum1 = (sum1 & 0xff) + (sum1 >> 8);
        sum2 = (sum2 & 0xff) + (sum2 >> 8);
    }

    // Second reduction step to reduce sums to 8 bits
    sum1 = (sum1 & 0xff) + (sum1 >> 8);
    sum2 = (sum2 & 0xff) + (sum2 >> 8);

    return (sum2 << 8) | sum1;
}

function introduceNoise(data) {
    // Convert the string to an array so we can modify it
    let dataArray = Array.from(data);

    // Choose a random index
    let index = Math.floor(Math.random() * dataArray.length);

    // Flip the bit at the chosen index
    if (dataArray[index] === '0') {
        dataArray[index] = '1';
    } else if (dataArray[index] === '1') {
        dataArray[index] = '0';
    }

    // Convert the array back to a string
    let noisyData = dataArray.join('');

    return noisyData;
}


//client side

const io = require('socket.io-client');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const sio = io.connect('http://0.0.0.0:3000');
const user = 'Jorge';

sio.on('connect', () => {
    console.log("Conectado al servidor!");
    messageLoop();
});

sio.on('mensaje_servidor', (msg) => {
    console.log("\n", msg);
});

function messageLoop() {
    rl.question("> ", (mensaje) => {

        let binary = stringToBinary(mensaje);
        let fletcher = fletcher16(binary);
        let jsonObj = {
            "message": binary,
            "fletCheck": fletcher
        };
        var message_send = JSON.stringify(jsonObj)
        console.log("Mensaje enviado: ", message_send);
        sio.emit('mensaje_python', message_send);
        if (mensaje === "/exit") {
            sio.emit('mensaje_python', `${user} se ha desconectado del servidor...`);
            rl.close();
            sio.disconnect();
        } else {
            messageLoop();
        }
    });
}


