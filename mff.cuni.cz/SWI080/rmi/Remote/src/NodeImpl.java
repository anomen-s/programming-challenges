import java.io.Serializable;
import java.util.HashSet;
import java.util.Set;

//  $Id: NodeImpl.java 77 2009-03-17 16:29:38Z ludek $

public class NodeImpl
implements Node, Serializable
{
    static final long serialVersionUID = 5636055143468530373L;
 
    private Set<Node> sNodes = new HashSet<Node>();

	public Set<Node> getNeighbors ()
	{
		return (sNodes);
	}

	public void addNeighbor (Node oNeighbor)
	{
		sNodes.add (oNeighbor);
	}
}

