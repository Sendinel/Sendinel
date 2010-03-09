import xmlrpclib

def set_connection_to_bluetooth(serverAddress):
    """
        Connect to the remote XML RPC server for bluetooth functionality
        
        @param  serverAddress:  FQDN or IP address of the remote host
        @type   serverAddress:  String
        
        @return: the XML RPC connection object
    """
    
    return xmlrpclib.ServerProxy('http://%s:8080' % serverAddress)
    
def get_discovered_devices(serverAddress):
    """
        Get a list of discovered bluetooth devices from the server
        
        @param  serverAddress:  FQDN or IP address of the remote host
        @type   serverAddress:  String
        
        @return:    Dictionary (MAC-Address -> Name)
    """
    
    conn = set_connection_to_bluetooth(serverAddress)
    return conn.Actions.getDiscoveredDevices()

def send_vcal(serverAddress, mac, data):
    """
        Send a ical/vcal file to a bluetooth device
    
        @param  serverAddress:  FQDN or IP address of the remote host
        @type   serverAddress:  String
        
        @param  mac:    MAC Address of the target bluetooth device
        @type   mac:    String
        
        @param  data:   plain text vcal data to be sent
        @type   data:   String
    """
    
    conn = set_connection_to_bluetooth(serverAddress)
    result = conn.Actions.sendVCalFile(mac, data, "reminder.vcs")