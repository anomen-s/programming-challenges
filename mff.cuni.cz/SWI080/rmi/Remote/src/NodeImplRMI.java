
import java.io.Serializable;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashSet;
import java.util.Set;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author hlavl1am
 */
public class NodeImplRMI extends UnicastRemoteObject implements Node/*, Serializable*/ {

    
    public NodeImplRMI()  throws RemoteException
    {
        super();
    }
    
    static final long serialVersionUID = 5636055143468530374L;
    private Set<Node> sNodes = new HashSet<Node>();


    public Set<Node> getNeighbors() {
        return sNodes;
    }

    public void addNeighbor(Node oNeighbor) {
        sNodes.add(oNeighbor);
    }

}

