package mwy;

import javax.ejb.Remote;

// Denotes remote interface by annotation
@Remote
public interface ExampleStateless {
	public String sayHello();
}
