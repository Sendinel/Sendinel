import xmlrpclib

def set_connection_to_bluetooth(server_address):
    """
        Connect to the remote XML RPC server for bluetooth functionality
        
        @param  server_address:  FQDN or IP address of the remote host
        @type   server_address:  String
        
        @return: the XML RPC connection object
    """
    
    return xmlrpclib.ServerProxy('http://%s:8080' % server_address)
    
def get_discovered_devices(server_address):
    """
        Get a list of discovered bluetooth devices from the server
        
        @param  server_address:  FQDN or IP address of the remote host
        @type   server_address:  String
        
        @return:    Dictionary (MAC-Address -> Name)
    """
    
    conn = set_connection_to_bluetooth(server_address)
    return conn.Actions.getDiscoveredDevices()

def send_vcal(server_address, mac, data):
    """
        Send a ical/vcal file to a bluetooth device
    
        @param  serverAddress:  FQDN or IP address of the remote host
        @type   serverAddress:  String
        
        @param  mac:    MAC Address of the target bluetooth device
        @type   mac:    String
        
        @param  data:   plain text vcal data to be sent
        @type   data:   String
    """
    
    conn = set_connection_to_bluetooth(server_address)
    result = conn.Actions.sendVCalFile(mac, data, "reminder.vcs")