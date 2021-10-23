package mwy;

import java.util.Random;
import java.util.List;
import java.util.HashSet;
import java.util.Set;
import javax.ejb.Stateful;
import javax.persistence.*;

@Stateful
public class SearcherBean implements Searcher
{
	//private Map<Integer, Node> nodeMap;

    	@PersistenceContext(unitName = "node-unit", type = PersistenceContextType.EXTENDED)
	private EntityManager entityManager;

	public SearcherBean() {
	//	nodeMap = new HashMap<Integer, Node>();
	}

	private Random oRandom = new Random ();

        public int getRandom()
        {
		Query query = entityManager.createQuery("SELECT n from Node as n ");
                List<Node> res = (List<Node>) query.getResultList();
		return res.get(oRandom.nextInt(res.size())).getId();

	}

        private Node getById(int id)
        {
//		Query query = entityManager.createQuery("SELECT n from Node as n WHERE id = :id");
//                query.setParameter("id", id);
//                return (Node) query.getSingleResult();
            return entityManager.find(Node.class, id);
        }
                
	public int getDistance (int idFrom, int idTo)
	{
		Node oFrom = getById(idFrom);
		Node oTo = getById(idTo);
		
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

			Set<Node> mTraversing = new HashSet<Node> ();

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

	public int addNode() {
                Node n = new Node();
                entityManager.persist(n);
		//nodeMap.put(n.getId(), n);
		return n.getId();
	}

	public void connectNodes(int nodeFrom, int nodeTo) {
		Node oFrom = getById(nodeFrom);//  nodeMap.get(nodeFrom);
		Node oTo =  getById(nodeTo);// nodeMap.get(nodeTo);

		oFrom.addNeighbor(oTo);
	}
	
}
