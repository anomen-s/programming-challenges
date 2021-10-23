import javax.jms.Connection;
import javax.jms.Message;
import javax.jms.MessageProducer;
import javax.jms.Queue;
import javax.jms.Session;

import org.apache.activemq.ActiveMQConnectionFactory;


public class ExampleProducer {
	
	public static void main(String[] args) {
		
		Connection connection = null;
		
		try {
			// Create connection to the broker.
			// Note that the factory is usually obtained from JNDI, this method is ActiveMQ-specific
			// used here for simplicity
			ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://localhost:61616");
			connection = connectionFactory.createConnection();
			connection.start();
			
			// Create a non-transacted, auto-acknowledged session
			Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			
			// Create a queue, name must match the queue created by consumer
			// Note that this is also provider-specific and should be obtained from JNDI
			Queue queue1 = session.createQueue("ExampleQueue1");
			
			// Create a producer for the queue
			MessageProducer producer1 = session.createProducer(queue1);
			
			// Create a message
			Message message1 = session.createTextMessage("ping");
			
			// Send the message
			producer1.send(message1);
			
			// Repeat all this with another queue
			Queue queue2 = session.createQueue("ExampleQueue2");
			MessageProducer producer2 = session.createProducer(queue2);
			Message message2 = session.createTextMessage("ping");
			producer2.send(message2);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				connection.close();
			} catch (Throwable ignore) {
			}
		}
	}
}
