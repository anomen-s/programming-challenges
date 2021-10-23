import java.rmi.RemoteException;

/**
  1. Seznamte se s poskytnutou implementaci ulohy, ktera pracuje lokalne.
     Zmerte rychlost provadeni na nekolika typech nahodne generovanych
     ridkych a hustych grafech.

 * $Id$
 */
public class Main extends Base {
    
    public static void main(String[] args) throws RemoteException {
        
        setSearcher(new SearcherImpl());
        graphInit(false);
        
        long t = searchBenchmark(SEARCHES);
        Stats.add("no rmi", t);
        
    }

}

