from pybleno import *
import sys
import signal
from EchoCharacteristic import *


uuid = "0000ec00-0000-1000-8000-00805f9b34fb"
characteristicId = "0000ec0f-0000-1000-8000-00805f9b34fb"

bleno = Bleno()

def onStateChange(state):
   print('on -> stateChange: ' + state)

   if (state == 'poweredOn'):
     print('Starting to advertise...')
     bleno.startAdvertising('echo', [uuid])
   else:
     print('Stopping advertising due to state change...')
     bleno.stopAdvertising()


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        print('Setting services...')
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': uuid,
                'characteristics': [
                    EchoCharacteristic(characteristicId)
                    ]
            })
        ])
    else:
        print('Error in advertising start: ', error)



bleno.on('stateChange', onStateChange)
bleno.on('advertisingStart', onAdvertisingStart)
bleno.start()

print ('Hit <ENTER> to disconnect')
input()

bleno.stopAdvertising()
bleno.disconnect()

print ('terminated.')
sys.exit(1)