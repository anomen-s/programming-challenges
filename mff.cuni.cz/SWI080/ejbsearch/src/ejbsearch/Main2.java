/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ejbsearch;

import java.util.Properties;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import local.*;
import mwy.Searcher;

/**
 *
 * @author hlavl1am
 */
public class Main2 extends Base {

      	public static void main (String[] args) throws NamingException
	{
            Properties props = new Properties();
            props.put(Context.INITIAL_CONTEXT_FACTORY, "org.apache.openejb.client.RemoteInitialContextFactory");
            props.put(Context.PROVIDER_URL, "ejbd://127.0.0.1:4201");
            Context ctx = new InitialContext(props);
            oSearcher = (Searcher) ctx.lookup("SearcherBeanRemote");

	    int n1 = oSearcher.getRandom();
	    int n2 = oSearcher.getRandom();
	    System.out.println("Nodes: "+n1+" " +n2);
            System.out.println(oSearcher.getDistance(n1,n2));

	}

}
