import re
import serial.tools.list_ports
import serial
from backend.Device.Device import Device 

# This class if for devices that use serial port profile (SPP)
class SerialDevice(Device):
    def __init__(self, name, address):
        super().__init__(name, address, "Serial")
    # Finds any necessary information needed about connecting to the device, finds sensor names and creates relevant client object    
    def connect(self ):
        try:
            self.serialObject = serial.Serial(self.Address, timeout=None)
            if not self.serialObject.is_open:
                print("Unable to open serial port")
            else:
                self.serialObject.reset_input_buffer()
                dataString = ""
                while dataString.count("\n") < 6:
                    numbytes = self.serialObject.in_waiting
                    byteString = self.serialObject.read(numbytes)
                    dataString += byteString.decode('utf-8')
                if dataString is not None and re.search("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString): 
                    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString)
                    for sensorName in sensorNames:
                        self.Sensors.add(sensorName)
                    self.serialObject.close()
                    return True 
                self.serialObject.close()
        except Exception as e:
            print(e)
        return False

    def getData(self):
        if not self.reconnect():
            self.serialObject = serial.Serial(self.Address, timeout=None) 
            print(f"Is port open: {self.serialObject.is_open}")
        self.serialObject.reset_input_buffer()
        while not self.TerminateSession.is_set():
            try:
                dataString = None
                while dataString is None:
                    numWaitingBytes = self.serialObject.in_waiting
                    dataString = self.serialObject.read(numWaitingBytes)
                dataString = dataString.decode('utf-8')
                if not self.isPaused():
                    self.addToDataBuffer(dataString)
            except:
                print("an error occurred") 
        self.disconnect()

    def reconnect(self):
        # This function aims to reconnect to the connected device (no information needs to be found just establish the connection again)
        if not self.serialObject.is_open:
            try:
                self.serialObject.open()
                return self.serialObject.is_open
            except:
                print("Error: could not reconnect")

            return False
        else:
            return True

    def isConnected(self):
        return self.serialObject.is_open

    def disconnect(self):
        print("disconnecting...")
        if self.serialObject.is_open:
            try:
                self.serialObject.close()
                print("disconnected")
                return True
            except:
                print("Error: could not disconnect")
        return False