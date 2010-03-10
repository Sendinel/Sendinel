import xmlrpclib

def set_connection_to_bluetooth(server_address):
    return xmlrpclib.ServerProxy('http://%s:8080' % server_address)
    
def get_discovered_devices(addressServer):
    conn = set_connection_to_bluetooth(addressServer)
    return conn.Actions.getDiscoveredDevices()

def send_vcal(server_address, mac, data):
    conn = set_connection_to_bluetooth(server_address)
    conn.Actions.sendVCalFile(mac, data, "reminder.vcs")