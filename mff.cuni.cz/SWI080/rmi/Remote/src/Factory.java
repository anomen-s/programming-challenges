
import java.rmi.Remote;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.

 * $Id: Factory.java 77 2009-03-17 16:29:38Z ludek $
 */
import java.rmi.RemoteException;

/**
 *
 * @author hlavl1am
 */
public interface Factory extends Remote {

    public Node createNode() throws RemoteException;
}

