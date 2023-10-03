const bleno = require('bleno');

const MY_SERVICE_UUID = '12ab';
const MY_CHARACTERISTIC_UUID = '34cd';

let myCharacteristic = new bleno.Characteristic({
    uuid: MY_CHARACTERISTIC_UUID,
    properties: ['read', 'write'],
    onWriteRequest: function(data, offset, withoutResponse, callback) {
        console.log('Data written:', data.toString());
        callback(this.RESULT_SUCCESS);
    }
});

bleno.on('stateChange', function(state) {
    console.log(`State change: ${state}`);

    if (state === 'poweredOn') {
        bleno.startAdvertising('MyService', [MY_SERVICE_UUID]);
    } else {
        bleno.stopAdvertising();
    }
});

bleno.on('advertisingStart', function(error) {
    console.log(`Advertising start: ${error ? 'error ' + error : 'success'}`);

    if (!error) {
        bleno.setServices([
            new bleno.PrimaryService({
                uuid: MY_SERVICE_UUID,
                characteristics: [myCharacteristic]
            })
        ]);
    }
});

// When someone connects, let's log it!
bleno.on('accept', function(clientAddress) {
    console.log(`Accepted connection from address: ${clientAddress}`);
});
