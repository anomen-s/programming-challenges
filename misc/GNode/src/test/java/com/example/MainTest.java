package com.example;

import java.util.ArrayList;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

/**
 *
 */
public class MainTest extends Assert {

    private static GNode graph;

    @BeforeClass
    public static void setUp() throws Exception {

        GNode E = new GNodeImpl("E");
        GNode F = new GNodeImpl("F");
        GNode G = new GNodeImpl("G");
        GNode H = new GNodeImpl("H");
        GNode I = new GNodeImpl("I");
        GNode J = new GNodeImpl("J");
        GNode B = new GNodeImpl("B", E, F);
        GNode C = new GNodeImpl("C", G, H, I);
        GNode D = new GNodeImpl("D", J);
        GNode A = new GNodeImpl("A", B, C, D);

        graph = A;

    }

    @Test
    public void testWalkGraph() throws Exception {

        Main main = new Main();

        final ArrayList<GNode> nodes = main.walkGraph(graph);

        assertEquals(10, nodes.size());

        String nodeNames = "ABCDEFGHIJ";
        for (int i = 0; i < nodeNames.length(); i++) {
            String n = nodeNames.substring(i,i+1);
            assertTrue("Missing " + n, nodes.toString().contains(n));
        }
        System.out.println(nodes);
    }

    @Test
    public void testPaths() throws Exception {
        Main main = new Main();

        final ArrayList<ArrayList<GNode>> paths = main.paths(graph);

        assertEquals(6, paths.size());
        assertEquals("[[A, B, E], [A, B, F], [A, C, G], [A, C, H], [A, C, I], [A, D, J]]", paths.toString());
        System.out.println(paths);

    }
}
