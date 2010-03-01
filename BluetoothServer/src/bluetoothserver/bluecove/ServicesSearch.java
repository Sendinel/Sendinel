package bluetoothserver.bluecove;
import java.io.IOException;
import javax.bluetooth.*;
/**
 *
 * Minimal Services Search example.
 */
public class ServicesSearch {

    static final UUID OBEX_OBJECT_PUSH = new UUID(0x1105);
    private static String serviceFoundURL = "";
    static final Object serviceSearchCompletedEvent = new Object();

    public static String searchServices(String mac) throws IOException, InterruptedException {

        serviceFoundURL = "";

        UUID serviceUUID = OBEX_OBJECT_PUSH;
        UUID[] searchUuidSet = new UUID[] { serviceUUID };
        int[] attrIDs =  new int[] {
                0x0100 // Service name
        };
        
        DiscoveryListener listener = createDiscoveryListener();

        if(! RemoteDeviceDiscovery.lastDevicesDiscovered.containsKey(mac) )
                                throw new IOException("MAC address not found");
        
        RemoteDevice btDevice = (RemoteDevice)
                RemoteDeviceDiscovery.lastDevicesDiscovered.get(mac);
        
        synchronized(serviceSearchCompletedEvent) {
            LocalDevice.getLocalDevice().getDiscoveryAgent()
                    .searchServices(attrIDs, searchUuidSet, btDevice, listener);
           
           serviceSearchCompletedEvent.wait();
        }
        
        return serviceFoundURL;
    }

    private static DiscoveryListener createDiscoveryListener() {
         return new DiscoveryListener() {

            public void deviceDiscovered(RemoteDevice btDevice, DeviceClass cod) {
            }

            public void inquiryCompleted(int discType) {
            }

            public void servicesDiscovered(int transID, ServiceRecord[] servRecord) {
                if(servRecord.length>0){
                    serviceFoundURL = servRecord[0].getConnectionURL(ServiceRecord.NOAUTHENTICATE_NOENCRYPT, false);
                }
            }

            public void serviceSearchCompleted(int transID, int respCode) {
                synchronized(serviceSearchCompletedEvent){
                    serviceSearchCompletedEvent.notifyAll();
                }
            }

        };
    }

}
