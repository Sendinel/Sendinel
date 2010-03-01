/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package bluetoothserver;

/**
 *
 * @author patrick
 */
public class Logging {
    public static void log (String e, int level){
        if(level>-1)
            System.out.println(e);
    }
}
