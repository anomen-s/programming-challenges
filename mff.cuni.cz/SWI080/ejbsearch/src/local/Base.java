package local;

import java.util.Random;

import mwy.Searcher;

public class Base 
{
	// How many nodes and how many edges to create.
	public static final int GRAPH_NODES = 50;
	public static final int GRAPH_EDGES = 100;

	// How many searches to perform
	public static final int SEARCHES = 50;
	
	public static Random oRandom = new Random ();
	public static Searcher oSearcher;
	
	private static int[] iNodeId;
	
	/**
	 * Creates nodes of a graph.
	 * @param iHowMany
	 */
	public static void createNodes (int iHowMany)
	{
		iNodeId = new int[iHowMany];
		
		for (int i = 0; i < iHowMany; i++)
		{
			int id = oSearcher.addNode();
			iNodeId[i] = id;
		}
	}
	
	/**
	 * Creates a randomly connected graph.
	 * @param iHowMany
	 */
	public static void connectSomeNodes (int iHowMany)
	{
		for (int i = 0; i < iHowMany; i++)
		{
			int iNodeFrom = iNodeId[oRandom.nextInt (iNodeId.length)];
			int iNodeTo = iNodeId[oRandom.nextInt (iNodeId.length)];

			oSearcher.connectNodes(iNodeFrom, iNodeTo);
		}
	}
	
	/**
	 * Runs a quick measurement on the graph.
	 * @param iHowMany
	 */
	public static void searchBenchmark (int iHowMany)
	{
		// Display measurement header.
		System.out.printf ("%7s %8s %13s\n", "Attempt", "Distance", "Time");
		for (int i = 0 ; i < iHowMany ; i ++)
		{
			// Select two random nodes.
			int iNodeFrom = iNodeId[oRandom.nextInt (iNodeId.length)];
			int iNodeTo = iNodeId[oRandom.nextInt (iNodeId.length)];

			// Calculate distance, timing the operation.
			long iTime = System.nanoTime ();
			int iDistance = oSearcher.getDistance (iNodeFrom, iNodeTo);
			iTime = System.nanoTime () - iTime;
			
			// Print the measurement result.
			System.out.printf ("%7d %8d %13d\n", i, iDistance, iTime / 1000);
		}        
	}

}
