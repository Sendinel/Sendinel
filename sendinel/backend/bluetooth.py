import xmlrpclib

def set_connection_to_bluetooth(addressServer):
    return xmlrpclib.ServerProxy('http://%s:8080' % addressServer)
    
def get_discovered_devices(addressServer):
    conn = set_connection_to_bluetooth(addressServer)
    return conn.Actions.getDiscoveredDevices()

def send_vcal(addressServer, mac, data):
    conn = set_connection_to_bluetooth(addressServer)
    result = conn.Actions.sendVCalFile(mac, data, "reminder.vcs")