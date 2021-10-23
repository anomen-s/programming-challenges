import java.rmi.RemoteException;
import java.util.HashSet;
import java.util.Set;

// $Id: SearcherImpl.java 77 2009-03-17 16:29:38Z ludek $

class SearcherImpl implements Searcher
{
	public int getDistance (Node oFrom, Node oTo) throws RemoteException
	{
		// Implements a trivial distance measurement algorithm.
		// Starting from the source node, a set of visited nodes
		// is always extended by immediate neighbors of all visited
		// nodes, until the target node is visited or no node is left.
		
		// mVisited keeps the nodes visited in past steps.
		// mBoundary keeps the nodes visited in current step.
		Set<Node> mVisited = new HashSet<Node> ();
		Set<Node> mBoundary = new HashSet<Node> ();

		int iDistance = 0;

		// We start from the source node.
		mBoundary.add (oFrom);

		// Traverse the graph until finding the target node.
		while (!mBoundary.contains (oTo))
		{
			// Not having anything to visit means the target node cannot be reached.
			if (mBoundary.isEmpty ())
				return (Searcher.DISTANCE_INFINITE);

			Set<Node> mTraversing = new HashSet <Node> ();

			// Collect a set of immediate neighbors of nodes visited in current step.
			for (Node oNode : mBoundary)
			{
				mTraversing.addAll (oNode.getNeighbors ());
			}
			
			// Nodes visited in current step become nodes visited in past steps.
			mVisited.addAll (mBoundary);
			// Out of immediate neighbors, consider only those not yet visited.
			mTraversing.removeAll (mVisited);
			// Make these nodes the new nodes to be visited in current step.
			mBoundary = mTraversing;

			iDistance ++;
		}

		return (iDistance);
	}
}

