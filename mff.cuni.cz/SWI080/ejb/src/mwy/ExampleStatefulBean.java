package mwy;

import javax.ejb.Stateful;

// Denotes a stateful session bean by annotation
@Stateful
public class ExampleStatefulBean implements ExampleStateful {

    // The field is part of the state that remains bound to a client instance
	private int count = 0;

	public int inc() {
		return ++count;
	}

	public int reset() {
		return (count = 0);
	}

}
