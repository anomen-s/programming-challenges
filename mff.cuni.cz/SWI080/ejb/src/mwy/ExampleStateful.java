package mwy;

import javax.ejb.Remote;

// Denotes remote interface by annotation
@Remote
public interface ExampleStateful {

	public int inc();

	public int reset();

}
