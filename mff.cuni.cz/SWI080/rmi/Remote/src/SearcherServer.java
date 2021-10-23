import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.RMISecurityManager;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.Random;
/**
  2. Vytvorte server, ktery bude poskytovat vzdalene pristupny objekt s
     rozhranim Searcher. Upravte poskytnutou implementaci ulohy tak, aby
     vedle dosavadnich funkci umoznila take nalezt vzdalenost pomoci
     serveroveho rozhrani Searcher, kteremu se jako graf predaji
     lokalni objekty s rozhranim Node.

     Zmerte a porovnejte rychlost implementovanych variant.
     Jak pristupuje Searcher na serveru k lokalnim objektum Node?

 * $Id: SearcherServer.java 78 2009-03-17 17:25:12Z ludek $
 */
public class SearcherServer
{
    public static final String RMI_LOCAL="ASSearcherServer";

  public static void main (String args [])
  { 
    // Create and install a security manager 
    if (System.getSecurityManager () == null)
    { 
      System.setSecurityManager (new RMISecurityManager()); 
    } 
    try
    { 
      ServerImpl obj = new ServerImpl(); 

//      Registry registry =  LocateRegistry.createRegistry( 1099);
//      registry.rebind (RMI_LOCAL, obj); 

      Naming.rebind("//127.0.0.1/"+RMI_LOCAL, obj);
	 

      System.out.println ("SearcherServer bound in registry as "+RMI_LOCAL);
    }
    catch (Exception e)
    { 
      System.out.println ("SearcherServer Exception: " + e.getMessage ()); 
      e.printStackTrace (); 
    } 
  } 
}

