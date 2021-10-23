import java.rmi.NotBoundException;
import java.rmi.Remote;
import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Random;
/*
 * Base.java
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

/**
 * $Id: Base.java 78 2009-03-17 17:25:12Z ludek $
 * @author ludek
 */
public class Base {

    public static  String RMI_HOST = "u-pl33.ms.mff.cuni.cz";
//    public static  String RMI_HOST = "localhost";
    public static  int  RMI_PORT = 1099;
    
//    public static  String RMI_HOST = "rmi://u1-7.ms.mff.cuni.cz:1099/";
    
    private static Random oRandom = new Random();
    
    // How many nodes and how many edges to create.
    public static final int GRAPH_NODES = 1000;
    public static final int GRAPH_EDGES = 2000;
    
    // How many searches to perform
    public static final int SEARCHES = 50;
    
    private static Node [] aNodes;
    
    public static Node[] getANodes() {
        return aNodes;
    }
    
    public static void setANodes(Node[] aANodes) {
        aNodes = aANodes;
    }
    
    private static Searcher searcher;
    
    public static Searcher getSearcher() {
        return searcher;
    }
    
    public static void setSearcher(Searcher aSearcher) {
        searcher = aSearcher;
    }
    

    public static Remote lookup() throws RemoteException, NotBoundException, java.net.MalformedURLException
    {
//        Registry registry=LocateRegistry.getRegistry(RMI_HOST, RMI_PORT );
//        return registry.lookup(SearcherServer.RMI_LOCAL);

        String name = "//" + RMI_HOST + "/" + SearcherServer.RMI_LOCAL;
        return Naming.lookup(name);
			
			

    }
    
    /** Creates a new instance of Tools */
    public Base() {
    }
    
    /**
     * Creates nodes of a graph.
     * @param iHowMany
     */
    public static void createNodes(int iHowMany) {
        aNodes = new Node [iHowMany];
        
        for (int i = 0 ; i < iHowMany ; i ++) {
            aNodes [i] = new NodeImpl();
        }
        
    }
    
    /**
     * Creates nodes of a remote graph.
     * @param f 
     * @param iHowMany
     * @throws java.rmi.RemoteException 
     */
    public static void createRemoteNodes(Factory f, int iHowMany) throws RemoteException {
        aNodes = new Node [iHowMany];
        
        for (int i = 0 ; i < iHowMany ; i ++) {
            aNodes [i] = f.createNode();
        }
        
    }

    /**
     * Creates a fully connected graph.
     */
    public static void connectAllNodes() throws RemoteException {
        for (int iNodeFrom = 0 ; iNodeFrom < aNodes.length ; iNodeFrom++) {
            for (int iNodeTo = iNodeFrom + 1 ; iNodeTo < aNodes.length ; iNodeTo++) {
                aNodes [iNodeFrom].addNeighbor(aNodes [iNodeTo]);
                aNodes [iNodeTo].addNeighbor(aNodes [iNodeFrom]);
            }
        }
    }
    
    /**
     * Creates a randomly connected graph.
     * @param iHowMany
     */
    public static void connectSomeNodes(int iHowMany) throws RemoteException {
        for (int i = 0 ; i < iHowMany ; i ++) {
            int iNodeFrom = oRandom.nextInt(aNodes.length);
            int iNodeTo = oRandom.nextInt(aNodes.length);
            
            aNodes [iNodeFrom].addNeighbor(aNodes [iNodeTo]);
        }
    }
    
    protected static void graphInit(boolean complete) throws RemoteException {
        // Create a randomly connected graph and do a quick measurement.
        // Consider replacing connectSomeNodes with connectAllNodes to
        // verify that all distances are equal to one.
        createNodes(GRAPH_NODES);
        if (complete) {
            connectAllNodes();
        } else {
            connectSomeNodes(GRAPH_EDGES);
        }
    }
    
    protected static void remoteGraphInit(Factory f, boolean complete) throws RemoteException {

        createRemoteNodes(f, GRAPH_NODES);
        if (complete) {
            connectAllNodes();
        } else {
            connectSomeNodes(GRAPH_EDGES);
        }
    }

    
    /**
     * Runs a quick measurement on the graph.
     * @param iHowMany
     * @return total time
     * @throws java.rmi.RemoteException 
     */
    public static long searchBenchmark(int iHowMany)
    throws RemoteException {
        // Display measurement header.
        System.out.printf("%7s %8s %13s\n", "Attempt", "Distance", "Time");
        
        long result = 0;
        
        for (int i = 0 ; i < iHowMany ; i ++) {
            // Select two random nodes.
            int iNodeFrom = oRandom.nextInt(aNodes.length);
            int iNodeTo = oRandom.nextInt(aNodes.length);
            
            // Calculate distance, timing the operation.
            long iTime = System.nanoTime();
            int iDistance = searcher.getDistance(aNodes [iNodeFrom], aNodes [iNodeTo]);
            iTime = System.nanoTime() - iTime;
            
            // Print the measurement result.
            System.out.printf("%7d %8d %13d\n", i, iDistance, iTime / 1000);
            
            result += iTime;
        }
        System.out.printf("Total time: %,d ms\n", (result / 1000000));
        return result;
    }
    
}

