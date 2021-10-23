package client;

import java.util.List;
import java.util.Properties;

import javax.naming.Context;
import javax.naming.InitialContext;

import mwy.ExampleEntities;
import mwy.ExampleStateful;
import mwy.ExampleStateless;

public class ExampleClient{
	public static void main(String[] args) throws Exception {
		// Obtain a JNDI context of the local OpenEJB server
		Properties props = new Properties();
		props.put(Context.INITIAL_CONTEXT_FACTORY, "org.apache.openejb.client.RemoteInitialContextFactory");
		props.put(Context.PROVIDER_URL, "ejbd://127.0.0.1:4201");
		Context ctx = new InitialContext(props);

		// Look up the stateless bean example
		ExampleStateless stateless = (ExampleStateless) ctx.lookup("ExampleStatelessBeanRemote");
		// Perform operation on the stateless bean
		String result = stateless.sayHello();
		System.out.println(result);

		// Look up the stateful session bean example
		ExampleStateful stateful = (ExampleStateful) ctx.lookup("ExampleStatefulBeanRemote");
		// Notice how each run of the client will have the same output
		// Because state of the bean is kept separately for each client run
		System.out.println(stateful.inc());
		System.out.println(stateful.inc());
		System.out.println(stateful.reset());
		System.out.println(stateful.inc());

		// Look up the stateful bean that operates with entity beans
		ExampleEntities movies = (ExampleEntities) ctx.lookup("ExampleEntityBeansRemote");

		// Add some data
		int d1 = movies.addDirector("Quentin Tarantino");
		movies.addMovie("Pulp Fiction", d1);
		movies.addMovie("Jackie Brown", d1);
		int d2 = movies.addDirector("Joel Coen");
		movies.addMovie("Fargo", d2);
		movies.addMovie("Big Lebowski", d2);

		// List the data
		// Notice how the list grows with multiple client runs because directors / movies
		// have an extra integer as a primary key, and not the names
		// Also notice that stopping and restarting the EJB server does not forget
		// the data thanks to the persistence
		List<String> list = movies.getDirectors();
		for (String d : list) {
			System.out.println(d);
		}
		list = movies.getDirectorsWithMovies();
		for (String d : list) {
			System.out.println(d);
		}
	}
}
