import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.Set;

// $Id: Node.java 77 2009-03-17 16:29:38Z ludek $

public interface Node extends Remote {
    
    Set<Node> getNeighbors()  throws RemoteException;
    void addNeighbor(Node oNeighbor) throws RemoteException;
}

