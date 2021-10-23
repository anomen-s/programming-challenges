/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

// $Id$

package local;

/**
 *
 * @author ludek
 * @version $Rev$
 */
public class Main extends Base {

    	public static void main (String[] args)
	{
		// Create a randomly connected graph and do a quick measurement.
		// Consider replacing connectSomeNodes with connectAllNodes to
		// verify that all distances are equal to one.
            
		oSearcher = new mwy.SearcherImpl ();
		createNodes (GRAPH_NODES);
		connectSomeNodes (GRAPH_EDGES);
		searchBenchmark (SEARCHES);
	}

}
