from pybleno import *
import sys
import signal
from EchoCharacteristic import *

print('bleno - echo')

bleno = Bleno()

uuid = "0000ec00-0000-1000-8000-00805f9b34fb"
characteristicId = "0000ec0f-0000-1000-8000-00805f9b34fb"

def onStateChange(state):
   print('on -> stateChange: ' + state)

   if (state == 'poweredOn'):
     bleno.startAdvertising('echo', [uuid])
   else:
     bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': uuid,
                'characteristics': [
                    EchoCharacteristic(characteristicId)
                    ]
            })
        ])
bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()

print ('Hit <ENTER> to disconnect')

if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

print ('terminated.')
sys.exit(1)