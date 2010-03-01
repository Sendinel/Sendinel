import unittest
import sendinel.backend.bluetooth

class BluetoothTest(unittest.TestCase):
    """
    """
    
    devices = {}
    def setUp(self):
        pass
    
    def test_discoveredDevices(self):
        
        BluetoothTest.devices = {'00A48F': 'super Handy'}
        self.addressServer = "127"
        
        class Action:
            def getDiscoveredDevices(self):
                return BluetoothTest.devices
        class Connection:
            Actions = Action()
            
            
        def set_conn(addressServer):
            return Connection()
      
        temp = sendinel.backend.bluetooth.set_connection_to_bluetooth
        sendinel.backend.bluetooth.set_connection_to_bluetooth = set_conn

       
        result = sendinel.backend.bluetooth.get_discovered_devices(self.addressServer)
        self.assertEquals(result, self.devices)

        sendinel.backend.bluetooth.set_connection_to_bluetooth = temp
    
    def test_sendVCalFile(self):
        BluetoothTest.mac = "00A48F"
        BluetoothTest.data = "Das ist eine VCS"
        BluetoothTest.filename = "reminder.vcs"
        BluetoothTest.addressServer = "127"
        
        class Action:
            def sendVCalFile(self, mac, data, filename):
                BluetoothTest.macResult = mac
                BluetoothTest.dataResult = data
                BluetoothTest.filenameResult = filename
        class Connection:
            Actions = Action()
            
        def set_conn(addressServer):
            return Connection()

        temp = sendinel.backend.bluetooth.set_connection_to_bluetooth
        sendinel.backend.bluetooth.set_connection_to_bluetooth = set_conn
        
        
        sendinel.backend.bluetooth.send_vcal(BluetoothTest.addressServer,
                                            BluetoothTest.mac,
                                            BluetoothTest.data)
        self.assertEquals(BluetoothTest.mac, BluetoothTest.macResult);
        self.assertEquals(BluetoothTest.data, BluetoothTest.dataResult);
        self.assertEquals(BluetoothTest.filename, BluetoothTest.filenameResult);

        sendinel.backend.bluetooth.set_connection_to_bluetooth = temp