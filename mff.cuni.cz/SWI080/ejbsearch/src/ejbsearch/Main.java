/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package ejbsearch;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.util.Properties;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import local.Base;
import mwy.Searcher;

/**
 *
 * @author ludek
 */
public class Main extends Base {

    private static LineNumberReader in = new LineNumberReader(new InputStreamReader(System.in));

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws NamingException, IOException {

        {

            Properties props = new Properties();
            props.put(Context.INITIAL_CONTEXT_FACTORY, "org.apache.openejb.client.RemoteInitialContextFactory");
            props.put(Context.PROVIDER_URL, "ejbd://127.0.0.1:4201");
            Context ctx = new InitialContext(props);

            oSearcher = (Searcher) ctx.lookup("SearcherBeanRemote");

            System.out.println("create...");
            createNodes(GRAPH_NODES);
            System.out.println("connect...");
            connectSomeNodes(GRAPH_EDGES);
            System.out.println("search...");
            searchBenchmark(SEARCHES);
        }
/*        System.out.println("<Enter>");
        in.read();
        {
            Properties props = new Properties();
            props.put(Context.INITIAL_CONTEXT_FACTORY, "org.apache.openejb.client.RemoteInitialContextFactory");
            props.put(Context.PROVIDER_URL, "ejbd://127.0.0.1:4201");
            Context ctx = new InitialContext(props);
            System.out.println("search...");
            oSearcher = (Searcher) ctx.lookup("SearcherBeanRemote");
            searchBenchmark(SEARCHES);
        }*/

    }
}
