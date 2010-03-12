package bluetoothserver;
import bluetoothserver.bluecove.*;
import java.util.Map;
import javax.bluetooth.RemoteDevice;
import java.io.IOException;
import java.util.HashMap;
import java.util.Set;
import java.util.Iterator;

/**
 * Define XML RPC methods
 */
public class Actions {
    private static final Object bluetoothInUse = new Object();

   /**
    * Return the discovered Bluetooth Devices.
    * @return HashMap   A HashMap List, contains the name and mac for the discovered Devices
    * @throws IOException
    * @throws InterruptedException
    */
    public Map getDiscoveredDevices()throws Exception {
        try{
        if(RemoteDeviceDiscovery.lastDevicesDiscoveredError) {
            throw new Exception("Device Discovery failed.");
        }
        HashMap deviceMap = new HashMap();
        synchronized(RemoteDeviceDiscovery.lastDevicesDiscovered){
            Set s = RemoteDeviceDiscovery.lastDevicesDiscovered.keySet();
            Iterator i = s.iterator();
            while(i.hasNext()){

               RemoteDevice btDevice = (RemoteDevice)
                       RemoteDeviceDiscovery.lastDevicesDiscovered.get(i.next());
               
               deviceMap.put(btDevice.getBluetoothAddress(),
                             btDevice.getFriendlyName(false));
            }
        }
        return deviceMap;
        } catch(Exception e){
            return new HashMap();
        }
    }

    /**
     * Sends plain text data via OBEX Push.
     */
    public String sendTextFile(String mac, String data, String filename) throws Exception{
        return sendFile(mac, data, filename, "text/plain");
    }

    /**
     * Sends a vCalender file via OBEX Push.
     */
    public String sendVCalFile(String mac, String data, String filename) throws Exception{
        System.out.println(data);
        return sendFile(mac, data, filename, "text/x-vCalendar");
    }

    /**
     * Sends a JPEG image via OBEX Push.
     */
    public String sendJPEGFile(String mac, byte[] data, String filename) throws Exception {
        return sendFile(mac, data, filename, "image/jpeg");
    }
    
    /**
     * Send data to a Bluetooth Device via OBEX Push.
     * @param mac   A String with the bluetooth MAC Address of the target device
     * @param data  A String with Data for the file
     * @param filename
     * @param filetype A string containint the MIME filetype.
     * @return boolean true if the File was succesfully sent
     * @throws Exception
     */
    private String sendFile(String mac, byte[] data,
                             String filename, String filetype) throws Exception {
        try{
            synchronized(bluetoothInUse) {

                RemoteDeviceDiscovery.disable();
                //Now Bluetooth is free
                System.out.println(mac);
                System.out.println(filename);
                System.out.println(filetype);
                //Send File to the Device
                String url = ServicesSearch.searchServices(mac);
                System.out.println(url);
                ObexPutClient.send(url, data, filename, filetype);
                return "done";
            }
        }catch(Exception e){
            return e.toString();
        }finally{
            //start Inquiry
            RemoteDeviceDiscovery.enable();
        }
        
    }

    /**
     * Overloaded sendFile to send a String instead of byte[] data.
     * @param data A string containing the data to be sent.
     * @throws Exception
     */
    private String sendFile(String mac, String data,
                             String filename, String filetype) throws Exception{
        return sendFile(mac, data.getBytes("iso-8859-1"), filename, filetype);
    }
}

