from pybleno import Characteristic
import array
import struct
import sys
import traceback

class EchoCharacteristic(Characteristic):

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
          })

        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('EchoCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data

        hexValue = [hex(c) for c in self._value]
        received_text = self._value.decode('utf-8')

        print('EchoCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], received_text))

        if self._updateValueCallback:
            print('EchoCharacteristic - onWriteRequest: notifying')

            self._updateValueCallback(self._value)

        callback(Characteristic.RESULT_SUCCESS)
