
import java.rmi.RemoteException;
import java.util.HashMap;
import java.util.Map;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
import java.util.Map.Entry;

/**
 *
 * @author ludek
 */
public class Stats {

    private static Map<String, Long> results = new HashMap<String, Long>();
    
    public static void add(String key, long value)
    {
        results.put(key, Long.valueOf(value));
    }
    
    
    public static void main(String[] args) throws RemoteException {
        Main.main(args);
        MainSearcherClient.main(args);
        MainNodeClient.main(args);
        MainClientOnly.main(args);
        
        System.out.println("------------------");
            
        for (Entry<String,Long> e : results.entrySet() ) {
            System.out.println(e.getKey()+ " : " + (e.getValue()/1000000));
        }
    }
}

