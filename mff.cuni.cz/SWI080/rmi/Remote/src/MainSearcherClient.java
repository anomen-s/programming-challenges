
import java.rmi.Naming;
import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
/**
  2. Vytvorte server, ktery bude poskytovat vzdalene pristupny objekt s
     rozhranim Searcher. Upravte poskytnutou implementaci ulohy tak, aby
     vedle dosavadnich funkci umoznila take nalezt vzdalenost pomoci
     serveroveho rozhrani Searcher, kteremu se jako graf predaji
     lokalni objekty s rozhranim Node.

     Zmerte a porovnejte rychlost implementovanych variant.
     Jak pristupuje Searcher na serveru k lokalnim objektum Node?

 * $Id: MainSearcherClient.java 77 2009-03-17 16:29:38Z ludek $
 */
public class MainSearcherClient extends Base {

    public static void main(String[] args) throws RemoteException {
        
        graphInit(false);

        // Create and install a security manager
        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new RMISecurityManager());
        }
        try {
            Searcher obj = (Searcher) lookup();
	  
            setSearcher(obj);
		             
            long t = searchBenchmark(SEARCHES);
            Stats.add("rmi searcher", t);
            
        } catch (Exception e) {
            System.out.println("SearcherClient Exception: " + e.getMessage());
            e.printStackTrace();
        }

    }
}

