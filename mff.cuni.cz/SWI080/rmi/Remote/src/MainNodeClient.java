
import java.rmi.Naming;
import java.rmi.RMISecurityManager;
import java.rmi.RemoteException;

/**
  3. Upravte server tak, aby poskytoval vzdalene pristupne objekty s
     rozhranim Node, ktere budou vytvareny na zadost klienta. Upravte
     poskytnutou implementaci ulohy tak, aby vedle dosavadnich funkci
     umoznila take nalezt vzdalenost pomoci lokalniho rozhrani Searcher,
     kteremu se jako graf predaji serverove objekty s rozhranim Node.

     Zmerte a porovnejte rychlost implementovanych variant.
     Jak pristupuje lokalni Searcher k objektum Node na serveru?

 * $Id: MainNodeClient.java 77 2009-03-17 16:29:38Z ludek $
 */
public class MainNodeClient extends Base {


    public static void main(String[] args) throws RemoteException {
        

        // Create and install a security manager
        if (System.getSecurityManager() == null) {
            System.setSecurityManager(new RMISecurityManager());
        }
        try {
    	    setSearcher(new SearcherImpl());

            Factory f = (Factory) lookup();

            remoteGraphInit(f, false);

            long t = searchBenchmark(SEARCHES);
            Stats.add("RMI nodes", t);
            
            
        } catch (Exception e) {
            System.out.println("NodeClient Exception: " + e.getMessage());
            e.printStackTrace();
        }

    }
}

