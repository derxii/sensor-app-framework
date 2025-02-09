from bleak import BleakScanner, BleakClient
import asyncio
import re
from backend.Device.Device import Device

class BluetoothDevice(Device):
    def __init__(self, name, address):
        self.characteristicUUID = ""
        self.characteristicProp = []
        self.client = None
        self.Method = ""  # This indicates if the sensor data is received via notifications or the GATT read command
        super().__init__(name, address, "Bluetooth")

    def callback(self, sender, data):
        try:
            if not self.isPaused():
                dataString = data.decode('utf-8')
                self.addToDataBuffer(dataString)
        except:
            print("cannot convert notification to utf-8", flush=True)
        
    # Finds any necessary information needed about connecting to the device, finds sensor names and may create relevant client object
    async def connect(self):
        success = False
        # iterate through all uuids and subscribe to notifications and check the data format to see if the characteristic uuid is correct
        if await BleakScanner.find_device_by_address(self.Address):
            try:
                client = BleakClient(self.Address)
                self.client = client
                await client.connect()
                # Get the services and characteristics
                services = await client.get_services()
                for service in services:
                    for characteristic in service.characteristics:
                        self.setDataBuffer("")
                        if "notify" in characteristic.properties or "read" in characteristic.properties:
                            if "notify" in characteristic.properties:
                                await client.start_notify(
                                    characteristic.uuid, self.callback
                                )
                                await asyncio.sleep(1)
                                print("subscribing to notifications")
                            try:
                                print(f"connection status: {client.is_connected}")
                                data = None
                                while data is None:
                                    data = await client.read_gatt_char(
                                        characteristic.uuid
                                    )
                                try:
                                    notificationDataString = self.getDataBuffer()
                                    print(notificationDataString)
                                    if re.search(
                                        "\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*",
                                        notificationDataString,
                                    ):
                                        self.characteristicUUID = characteristic.uuid
                                        dataString = notificationDataString
                                        self.characteristicProp = (
                                            characteristic.properties
                                        )
                                        print("found characteristic")
                                        success = True
                                        self.Method = "notify"
                                        print("Method is notify")
                                        while self.getDataBuffer().count("\n") < 2:
                                            await asyncio.sleep(0.05)
                                        await client.stop_notify(characteristic.uuid)
                                except:
                                    print("invalid notification string")

                                if not success:
                                    try:
                                        readDataString = data.decode("utf-8")
                                        if re.search(
                                            "\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*",
                                            readDataString,
                                        ):
                                            self.characteristicUUID = (
                                                characteristic.uuid
                                            )
                                            dataString = readDataString
                                            self.characteristicProp = (
                                                characteristic.properties
                                            )
                                            print("found characteristic")
                                            success = True
                                            self.Method = "read"
                                            print("Method is read")
                                    except:
                                        print("invalid read string")

                                if success:
                                    sensorNames = re.findall(
                                        "\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", dataString
                                    )
                                    for sensorName in sensorNames:
                                        self.Sensors.add(sensorName)

                                if (
                                    "notify" in characteristic.properties
                                    and not success
                                ):
                                    await client.stop_notify(characteristic.uuid)
                                    print("unsubscribing from notifications")
                                if success and client.is_connected:
                                    self.setDataBuffer("")
                                    return success
                            except: 
                                print("error occurred")            
            except:
                print("Unable to connect")
        return success

    async def reconnect(self):
        # This function aims to reconnect to the connected device (no information needs to be found just establish the connection again)
        if await BleakScanner.find_device_by_address(self.Address):
            try:
                client = BleakClient(self.Address)
                self.client = client
                await self.client.connect()
                return self.client.is_connected
            except:
                print("Error: could not connect to device")
        else:
            print("Error: device address not found")
        return False

    def isConnected(self):
        return self.client.is_connected

    async def disconnect(self):
        if self.client.is_connected:
            try:
                print("disconnecting")
                await self.client.disconnect()
                print("disconnected")
                return not self.client.is_connected
            except:
                print("Error: could not disconnect")
        return False

    async def getData(self):
        self.setDataBuffer("")
        await self.client.start_notify(self.characteristicUUID, self.callback)
        while not self.TerminateSession.is_set():
            await asyncio.sleep(0.5)   
        await self.client.stop_notify(self.characteristicUUID)
        await asyncio.sleep(0.5)
        print("unsubscribing to notifications")