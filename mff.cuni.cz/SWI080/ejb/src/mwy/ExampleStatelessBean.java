package mwy;

import javax.ejb.Stateless;

// Denotes stateless session bean by annotation
@Stateless
public class ExampleStatelessBean implements ExampleStateless {
	public String sayHello() {
		return "Hello World!!!!";
	}
}
