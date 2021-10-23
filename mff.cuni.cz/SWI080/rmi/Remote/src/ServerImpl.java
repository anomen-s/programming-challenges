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

 * $Id: ServerImpl.java 81 2009-03-17 17:43:39Z ludek $
 */
public class ServerImpl
  extends UnicastRemoteObject
  implements Searcher, Factory
{

    public Node createNode() throws RemoteException {
        return new NodeImplRMI();
    }


  public ServerImpl () throws RemoteException { super (); }

  Searcher s = new SearcherImpl();

  public int getDistance (Node oFrom, Node oTo) throws RemoteException
  {
      System.out.println(System.nanoTime() + " ServerIml.getDistance "+oFrom.toString() + " - " + oTo.toString());
      return s.getDistance(oFrom, oTo);
  }

}

