package mwy;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

public class Node
{
	private int id;
	
	private Set<Node> sNodes = new HashSet<Node>();

	public Node(int id) {
		this.id = id;
	}
	
	public Collection<Node> getNeighbors ()
	{
		return (sNodes);
	}
	
	public void addNeighbor (Node oNeighbor)
	{
		sNodes.add (oNeighbor);
	}
}
