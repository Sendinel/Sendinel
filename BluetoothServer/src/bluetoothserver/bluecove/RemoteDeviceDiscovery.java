package bluetoothserver.bluecove;

import java.util.*;
import javax.bluetooth.*;
import com.intel.bluetooth.BlueCoveImpl;

/**
 * RemoteDeviceDiscover constantly tries to discover BluetoothDevices.
 * Example usage:
 *  RemoteDeviceDiscovery.run();
 */
public class RemoteDeviceDiscovery {
    public static Map lastDevicesDiscovered = Collections.synchronizedMap(new HashMap());
    public static boolean lastDevicesDiscoveredError = false;
    private static boolean disabled = false;
    private static Map devicesDiscovered = Collections.synchronizedMap(new HashMap());
    private static DiscoveryListener listener;
    private static final Object inquiryCompletedEvent = new Object();
    private static long startTime;
    private static final int waitForRestart = 20000;

    /**
     * start device discovery, runs infinite
     * @throws java.lang.InterruptedException
     */
    public static void run() throws java.lang.InterruptedException{

        while(true){
            try{
                if(!RemoteDeviceDiscovery.disabled){
                    RemoteDeviceDiscovery.discoverDevices();
                    RemoteDeviceDiscovery.waitForDeviceDescoveryCompleted();
                }else{
                    Thread.sleep(1000);
                }
            }catch(Exception e ){
                bluetoothserver.Logging.log("error during Device Discovery "
                                            + e.getMessage(), 1);
                Thread.sleep(1000);
            }
        }
    }
    
    /**
     * Start one asynchronous device discovery run.
     * @throws Exception
     */
    public static void discoverDevices() throws Exception {
        devicesDiscovered = Collections.synchronizedMap(new HashMap());
        listener = createDiscoveryListener();

        synchronized(inquiryCompletedEvent) {
            bluetoothserver.Logging.log("starting inquiry...", 0);
            startTime = System.currentTimeMillis();
            boolean started = LocalDevice.getLocalDevice().getDiscoveryAgent()
                                    .startInquiry(DiscoveryAgent.GIAC, listener);
            if (!started)
                throw new Exception("error while starting inquiry...");
        }
    }

    /**
     * Initialize a DiscoveryListener, implements daviceDiscovered and inquiryCompleted
     * @return  DiscoveryListener
     */
    private static DiscoveryListener createDiscoveryListener(){
        return new DiscoveryListener() {

            /**
             * Save discovered Devices in the devicesDiscovered Vector.
             */
            public void deviceDiscovered(RemoteDevice btDevice, DeviceClass cod) {
               bluetoothserver.Logging.log("Device "
                       + btDevice.getBluetoothAddress() + " found", 0);
                //devicesDiscovered.addElement(btDevice);
                String mac = btDevice.getBluetoothAddress();
                String name = "";
                try {
                     name = btDevice.getFriendlyName(false);
                } catch (Exception e) {}
                devicesDiscovered.put(mac, btDevice);
                lastDevicesDiscovered.put(mac, btDevice);
            }

            /**
             * handle inquiry results - copy devicesDiscovered
             * to public lastDevicesDiscovered.
             */
            public void inquiryCompleted(int discType) {
                bluetoothserver.Logging.log("Device Inquiry completed!",0);
                synchronized(inquiryCompletedEvent){
                    try {
                        if(!RemoteDeviceDiscovery.disabled) {
                            lastDevicesDiscovered = devicesDiscovered;


                            if(wasExecutionTimeTooShort())
                                restartBlueCove();
                        }
                        lastDevicesDiscoveredError = (discType == INQUIRY_ERROR);

                    } catch(Exception e) {
                        bluetoothserver.Logging.log("error during restarting Device Discorvery"
                                                     + e.getMessage(), 1);
                    }
                    inquiryCompletedEvent.notifyAll();
                }
            }

            public void serviceSearchCompleted(int transID, int respCode) {
            }

            public void servicesDiscovered(int transID, ServiceRecord[] servRecord) {
            }
        };
    }
    /**
     * Enable the DeviceDiscovery.
     */
    public static void enable(){
        RemoteDeviceDiscovery.disabled = false;
    }
    
    /**
     * Disable the DeviceDiscovery and wait until it is canceled.
     * @throws BluetoothStateException
     * @throws java.lang.InterruptedException
     */
    public static void disable()
            throws BluetoothStateException, java.lang.InterruptedException {
        RemoteDeviceDiscovery.disabled = true;
        LocalDevice.getLocalDevice().getDiscoveryAgent().cancelInquiry(listener);
        synchronized(inquiryCompletedEvent){
            inquiryCompletedEvent.wait();
        }
    }

    /**
     * Wait for a DeviceDiscovery run to complete.
     * @throws java.lang.InterruptedException
     */
    public static void waitForDeviceDescoveryCompleted()
             throws java.lang.InterruptedException {
        synchronized(inquiryCompletedEvent){
            inquiryCompletedEvent.wait();
        }
    }

    /**
     * Workaround for buggy bluetooth stack.
     * Check wheather DeviceDiscovery ran shorter than one second
     * @return  boolean
     */
    private static boolean wasExecutionTimeTooShort(){
        long interval = 1000;
        long timeElapsed = System.currentTimeMillis() - startTime;

        return (timeElapsed < interval);
    }

    /**
     * Workaround for buggy bluetooth stack.
     * Shutdown BlueCove and wait waitForRestart seconds.
     * @throws java.lang.InterruptedException
     */
    private static void restartBlueCove() throws java.lang.InterruptedException {
        bluetoothserver.Logging.log("discovery execution time too short, restarting Bluetooth Stack in "
                                     + waitForRestart + " milliseconds", 1);
        BlueCoveImpl.shutdown();
        Thread.sleep(waitForRestart);
    }
}
