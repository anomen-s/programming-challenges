package client;

import java.io.Serializable;


public class Goods implements Serializable {

	private static final long serialVersionUID = 8409458516353803478L;

	public final String name;
	
	public final int price;
	
	public Goods(String name, int price) {
		this.name = name;
		this.price = price;
	}
	
	@Override
	public String toString() {
		return name + " : $" + String.valueOf(price);
	}
}
