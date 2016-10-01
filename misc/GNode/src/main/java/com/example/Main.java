package com.example;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Set;

public class Main {

    /**
     * return a ArrayList containing every GNode in the
     *   graph. Each node appears in the ArrayList exactly once
     *   (i.e. no duplicates).
     * @param node root node
     * @return List of all nodes
     */
    public ArrayList<GNode> walkGraph(GNode node) {

        final LinkedList<GNode> nodes = new LinkedList<GNode>();
        nodes.add(node);

        final Set<GNode> result = new HashSet<GNode>();

        while (!nodes.isEmpty()) {
            GNode nextNode = nodes.removeFirst();
            result.add(nextNode);
            for (GNode child : nextNode.getChildren()) {
                nodes.add(child);
            }
        }
        return new ArrayList<GNode>(result);
    }


    private static class NodePath {
        GNode node;
        /* path to parent of node */
        ArrayList<GNode> path;

        public NodePath(GNode node, ArrayList<GNode> path) {
            this.node = node;
            this.path = path;
        }
    }

    /**
     *  return a ArrayList of ArrayLists, representing all
     *   possible paths through the graph starting at 'node'. The ArrayList
     *   returned can be thought of as a ArrayList of paths, where each path
     *   is represented as an ArrayList of GNodes.
     *
     * @param node root node
     * @return List of paths from root node to each leaf
     */
    public ArrayList<ArrayList<GNode>> paths(GNode node) {

        final LinkedList<NodePath > nodes = new LinkedList<NodePath>();
        nodes.add(new NodePath(node, new ArrayList<GNode>()));

        final ArrayList<ArrayList<GNode>> result = new ArrayList<ArrayList<GNode>>();

        while (!nodes.isEmpty()) {
            NodePath n = nodes.removeFirst();
            n.path.add(n.node);

            if (n.node.getChildren().length == 0) {
                result.add(n.path);
            } else {

                for (GNode child : n.node.getChildren()) {
                    nodes.add(new NodePath(child, new ArrayList<GNode>(n.path)));
                }
            }
        }
        return result;
    }

}
