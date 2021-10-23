import java.rmi.Naming;
import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;

/**
  4. Doplnte jeste nalezeni vzdalenosti pomoci serveroveho rozhrani
     Searcher, kteremu se jako graf predaji serverove objekty s
     rozhranim Node.

     Zmerte a porovnejte rychlost implementovanych variant.
     Jak pristupuje Searcher na serveru k objektum Node na serveru?


 * $Id: MainClientOnly.java 77 2009-03-17 16:29:38Z ludek $
 */
public class MainClientOnly extends Base {

    
    public static void main(String[] args) throws RemoteException {
        

        // Create and install a security manager
        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new RMISecurityManager());
        }
        try {
            Searcher s = (Searcher) lookup();
            setSearcher(s);
            
            Factory f = (Factory) lookup();
            remoteGraphInit(f, false);
            
            long t = searchBenchmark(SEARCHES);
            Stats.add("nodes/searcher RMI", t);
            
            
        } catch (Exception e) {
            System.out.println("OnlyClient Exception: " + e.getMessage());
            e.printStackTrace();
        }

    }
}

