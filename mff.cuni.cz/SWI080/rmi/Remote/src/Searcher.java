
import java.rmi.Remote;
import java.rmi.RemoteException;

// $Id: Searcher.java 77 2009-03-17 16:29:38Z ludek $

public interface Searcher extends Remote {
    public static final int DISTANCE_INFINITE = -1;
    public int getDistance(Node oFrom, Node oTo) throws RemoteException;
    
}

