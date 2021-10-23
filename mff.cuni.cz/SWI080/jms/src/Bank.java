import java.util.HashMap;
import java.util.Map;

import javax.jms.*;

import org.apache.activemq.ActiveMQConnectionFactory;

public class Bank implements MessageListener {
	
	/**** PUBLIC CONSTANTS ****/

	// text message command open new account
	public static final String NEW_ACCOUNT_MSG = "NEW_ACCOUNT";
	
	// MapMessage key for order type 
	public static final String ORDER_TYPE_KEY = "orderType";

	// order type "send money"
	public static final int ORDER_TYPE_SEND = 1;
	
	// MapMessage key for receiver's account number
	public static final String ORDER_RECEIVER_ACC_KEY = "receiverAccount";
	
	// MapMessage key for amount of money transfered 
	public static final String AMOUNT_KEY = "amount";
	
	// name of the queue for sending messages to Bank
	public static final String BANK_QUEUE = "BankQueue";

	// MapMessage key for report type
	public static final String REPORT_TYPE_KEY = "reportType";
	 
	// report type "received money"
	public static final int REPORT_TYPE_RECEIVED = 1;
	
	// MapMessage key for sender's account
	public static final String REPORT_SENDER_ACC_KEY = "senderAccount";
	
	/**** PRIVATE VARIABLES ****/

	// connection to broker
	private Connection conn;
	
	// session for asynchronous event messages
	private Session bankSession;
	
	// sender of (reply) messages, not bound to any destination
	private MessageProducer bankSender;

	// receiver of event messages
	private MessageConsumer bankReceiver;
	
	// Queue of incoming messages
	private Queue toBankQueue;
	
	// last assigned account number
	private int lastAccount;
	
	// map client names to client account numbers
	private Map<String, Integer> clientAccounts;
	
	// map client account numbers to client names
	private Map<Integer, String> accountsClients;
	
	// map client names to client report destinations
	private Map<String, Destination> clientDestinations;
	
	/**** PRIVATE METHODS ****/
	
	/*
	 * Constructor, stores broker connection and initializes maps
	 */
	private Bank(Connection conn) {
		this.conn = conn;
		
		// start with some arbitrary value
		lastAccount = 1000000;
		clientAccounts = new HashMap<String, Integer>();
		accountsClients = new HashMap<Integer, String>();
		clientDestinations = new HashMap<String, Destination>();
	}
	
	/*
	 * Initialize messaging structures, start listening for messages
	 */
	private void init() throws JMSException {
        // create a non-transacted, auto acknowledged session
        bankSession = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
        
        // create queue for incoming messages
        toBankQueue = bankSession.createQueue(BANK_QUEUE);

        // create consumer of incoming messages
        bankReceiver = bankSession.createConsumer(toBankQueue);
        
        // receive messages asynchronously, using this object's onMessage()
        bankReceiver.setMessageListener(this);
        
        // create producer of messages, not bound to any destination
        bankSender = bankSession.createProducer(null);
        
        // start processing incoming messages
        conn.start();
	}
	
	/*
	 * Handle text messages - in our case it's only the message requesting new account
	 */
	private void processTextMessage(TextMessage txtMsg) throws JMSException {
		// get the destination that client specified for replies
		// we will use it to send reply and also store it for transfer report messages
		Destination replyDest = txtMsg.getJMSReplyTo();
		// is it a NEW ACCOUNT message?
		if (NEW_ACCOUNT_MSG.equals(txtMsg.getText())) {
			// get the client's name stored as a property
			String clientName = txtMsg.getStringProperty(Client.CLIENT_NAME_PROPERTY);
			
			// store client's reply destination for future transfer reports
			clientDestinations.put(clientName, replyDest);
			
			int accountNumber;
			// either assign new account number or return already known number
			if (clientAccounts.get(clientName) != null) {
				accountNumber = clientAccounts.get(clientName);
			} else {
				accountNumber = lastAccount++;
				// also store the newly assigned number
				clientAccounts.put(clientName, accountNumber);
				accountsClients.put(accountNumber, clientName);
			}
			
			System.out.println("Connected client " + clientName + " with account " + accountNumber);
			
			// create reply TextMessage with the account number 
			TextMessage reply = bankSession.createTextMessage(String.valueOf(accountNumber));
			// send the reply to the provided reply destination
			bankSender.send(replyDest, reply);
		} else {
			System.out.println("Received unknown text message: " + txtMsg.getText());
			System.out.println("Full message info:\n" + txtMsg);
		}
	}
	
	/*
	 * Handle map messages - in our case it's only the message ordering money transfer to a receiver account
	 */
	private void processMapMessage(MapMessage mapMsg) throws JMSException {
		// get the order type number
		int order = mapMsg.getInt(ORDER_TYPE_KEY);
		
		// process order to transfer money
		if (order == ORDER_TYPE_SEND) {
			// get client's name
			String clientName = mapMsg.getStringProperty(Client.CLIENT_NAME_PROPERTY);
			
			// find client's account number
			int clientAccount = clientAccounts.get(clientName);
			
			// get receiver account number
			int destAccount = mapMsg.getInt(ORDER_RECEIVER_ACC_KEY);
			
			// find receiving client's name
			String destName = accountsClients.get(destAccount);
			
			// find receiving client's report message destination
			Destination dest = clientDestinations.get(destName);
			
			// get amount of money being transferred
			int amount = mapMsg.getInt(AMOUNT_KEY);
						
			System.out.println("Transferring $" + amount + " from account " + clientAccount + " to account " + destAccount);
			
			// create report message for the receiving client
			MapMessage reportMsg = bankSession.createMapMessage();
			
			// set report type to "you received money"
			reportMsg.setInt(REPORT_TYPE_KEY, REPORT_TYPE_RECEIVED);
			
			// set sender's account number
			reportMsg.setInt(REPORT_SENDER_ACC_KEY, clientAccount);
			
			// set money of amount transfered
			reportMsg.setInt(AMOUNT_KEY, amount);
			
			// send report to receiver client's destination
			bankSender.send(dest, reportMsg);
		} else {
			System.out.println("Received unknown MapMessage:\n" + mapMsg);
		}
	}
	
	/**** PUBLIC METHODS ****/
	
	/*
	 * React to asynchronously received message
	 */
	@Override
	public void onMessage(Message msg) {
		// distinguish type of message and call appropriate handler
		try {
			if (msg instanceof TextMessage) {
				processTextMessage((TextMessage) msg);
			} else if (msg instanceof MapMessage) {
				processMapMessage((MapMessage) msg);
			} else {
				System.out.println("Received unknown message:\n: " + msg);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * Main method, create connection to broker and a Bank instance
	 */
	public static void main(String[] args) {

		Connection connection = null;
		Bank bank = null;
		
		try {
            // create connection to the broker.
            ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://localhost:61616");
            connection = connectionFactory.createConnection();
            // create a bank instance
            bank = new Bank(connection);
            // initialize bank's messaging
            bank.init();
            
            // bank now listens to asynchronous messages on another thread
            // wait for user before quit
   			System.out.println("Bank running. Press enter to quit");
    			
   			System.in.read();
    			
   			System.out.println("Stopping...");
		}
		catch (Exception e) {
			e.printStackTrace();
		} finally {
	        try {
	        	// always close the connection
	            connection.close();
	        } catch (Throwable ignore) {
	        	// ignore errors during close
	        }
		}
	}
}
