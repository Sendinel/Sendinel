package bluetoothserver.bluecove;
import java.io.IOException;
import java.io.OutputStream;
import javax.microedition.io.Connector;
import javax.obex.*;

public class ObexPutClient {


    public static void send(String serverURL, byte[] data, String filename, String filetype) throws IOException, InterruptedException {

        bluetoothserver.Logging.log("Connecting to " + serverURL, 0);
        if(serverURL.equals("")) throw new IOException("error while connecting");
        ClientSession clientSession = (ClientSession) Connector.open(serverURL);
        HeaderSet hsConnectReply = clientSession.connect(null);
        
        if (hsConnectReply.getResponseCode() != ResponseCodes.OBEX_HTTP_OK) {
            bluetoothserver.Logging.log("Failed to connect", 1);
            return;
        }

        HeaderSet hsOperation = clientSession.createHeaderSet();
        hsOperation.setHeader(HeaderSet.NAME, filename);
        hsOperation.setHeader(HeaderSet.TYPE, filetype);
        hsOperation.setHeader(HeaderSet.LENGTH, new Long(data.length));

        //Create PUT Operation
        Operation putOperation = clientSession.put(hsOperation);

        // Send some text to server
        OutputStream os = putOperation.openOutputStream();
        os.write(data);
        os.close();
        putOperation.close();
        clientSession.disconnect(null);
        clientSession.close();
        bluetoothserver.Logging.log("sent", 0);
    }

}
