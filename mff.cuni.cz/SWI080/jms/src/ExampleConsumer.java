import javax.jms.Connection;
import javax.jms.Message;
import javax.jms.MessageConsumer;
import javax.jms.MessageListener;
import javax.jms.Queue;
import javax.jms.Session;
import javax.jms.TextMessage;

import org.apache.activemq.ActiveMQConnectionFactory;


public class ExampleConsumer implements MessageListener {
	
	public static void main(String[] args) {
		
		Connection connection = null;
		
		try {
			// Create connection to the broker.
			// Note that the factory is usually obtained from JNDI, this method is ActiveMQ-specific
			// used here for simplicity
			ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://localhost:61616");
			connection = connectionFactory.createConnection();
			
			// Create a non-transacted, auto-acknowledged session
			Session session1 = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			
			// Create a queue, name must match the queue created by producer
			// Note that this is also provider-specific and should be obtained from JNDI
			Queue queue1 = session1.createQueue("ExampleQueue1");
			
			// Create a consumer
			MessageConsumer consumer1 = session1.createConsumer(queue1);
			
			// Create and set an asynchronous message listener
			consumer1.setMessageListener(new ExampleConsumer());
			
			// Start processing messages
			connection.start();
			
			// Create another session, queue and consumer
			Session session2 = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			Queue queue2 = session2.createQueue("ExampleQueue2");
			MessageConsumer consumer2 = session2.createConsumer(queue2);
			
			// Receive a message synchronously
			Message msg = consumer2.receive();
			
			// Print the message
			if (msg instanceof TextMessage) {
				TextMessage txt = (TextMessage) msg;
				System.out.println("Synchronous: " + txt.getText());
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				connection.close();
			} catch (Throwable ignore) {
			}
		}
	}
	
	// Asynchronously receive messages
	public void onMessage(Message msg) {
		// Print the message
		try {
			if (msg instanceof TextMessage) {
				TextMessage txt = (TextMessage) msg;
				System.out.println("Asynchronous: " + txt.getText());
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
