const io = require('socket.io-client');
const socket = io.connect('http://192.168.1.33:4000');

socket.on('message', function(msg) {
    console.log('Trama con información adicional recibida: ' + msg);
    detectAndCorrectErrors(msg);
});

function detectAndCorrectErrors(hammingCode) {
    let r = 0;
    let m = hammingCode.length;

    while (Math.pow(2, r) < m + r + 1) {
        r++;
    }

    let errorDetected = false;
    let errorPosition = -1;

    for (let i = 0; i < r; i++) {
        let parity = 0;
        for (let j = 1; j <= m; j++) {
            if (j & Math.pow(2, i) === Math.pow(2, i)) {
                parity = parity ^ parseInt(hammingCode.charAt(m - j));
            }
        }

        if (parity !== parseInt(hammingCode.charAt(m - Math.pow(2, i)))) {
            errorDetected = true;
            errorPosition += Math.pow(2, i);
        }
    }

    if (errorDetected) {
        const correctedHammingCode = correctError(hammingCode, errorPosition);
        console.log('Se ha detectado y corregido un error en el bit ' + errorPosition);
        console.log('Trama corregida: ' + correctedHammingCode);
    } else {
        console.log('No se detectaron errores. Trama recibida: ' + hammingCode);
    }
}

function correctError(hammingCode, errorPosition) {
    const charArray = hammingCode.split('');
    charArray[errorPosition] = (charArray[errorPosition] === '0') ? '1' : '0';
    return charArray.join('');
}
