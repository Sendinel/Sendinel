package bluetoothserver;

import org.apache.xmlrpc.server.PropertyHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcServer;
import org.apache.xmlrpc.server.XmlRpcServerConfigImpl;
import org.apache.xmlrpc.webserver.WebServer;
import bluetoothserver.bluecove.*;

/**
 * XML RPC Server to provide bluetooth services
 */
public class BluetoothServer {
    private static int port = 8080;

    /**
     * Start the XML RPC Server and the background DeviceDiscovery.
     * @param args  Port the XML RPC Server listens on - default 8080.
     */
    public static void main(String[] args) {
        if(args != null && args.length > 0){
            port = Integer.parseInt(args[0]);
        }
        
        try{
          
          WebServer webServer = new WebServer(port);

          XmlRpcServer xmlRpcServer = webServer.getXmlRpcServer();
          PropertyHandlerMapping phm = new PropertyHandlerMapping();
          phm.addHandler("Actions", Actions.class);

          xmlRpcServer.setHandlerMapping(phm);

          XmlRpcServerConfigImpl serverConfig =
              (XmlRpcServerConfigImpl) xmlRpcServer.getConfig();
          serverConfig.setEnabledForExtensions(true);
          serverConfig.setContentLengthOptional(false);

          webServer.start();
          Logging.log("Server is running", 0);
          RemoteDeviceDiscovery.run();
          
        }catch(Exception e){
            bluetoothserver.Logging.log("error during XML RPC " + e.getMessage(), 1);
        }
    }


}
