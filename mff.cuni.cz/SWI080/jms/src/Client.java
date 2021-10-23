import java.io.IOException;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import javax.jms.*;

import org.apache.activemq.ActiveMQConnectionFactory;

public class Client {
	
	/****	CONSTANTS	****/
	
	// name of the property specifying client's name
	public static final String CLIENT_NAME_PROPERTY = "clientName";

	// name of the topic for publishing offers
	public static final String OFFER_TOPIC = "Offers";
	
	/****	PRIVATE VARIABLES	****/
	
	// client's unique name
	private String clientName;

	// client's account number
	private int accountNumber;
	
	// offered goods, mapped by name
	private Map<String, Goods> offeredGoods;
	
	// available goods, mapped by seller's name 
	private Map<String, List<Goods>> availableGoods;
	
	// reserved goods, mapped by name of the goods
	private Map<String, Goods> reservedGoods;
	
	// buyer's names, mapped by their account numbers
	private Map<Integer, String> reserverAccounts;
	
	// buyer's reply destinations, mapped by their names
	private Map<String, Destination> reserverDestinations;
	
	// connection to the broker
	private Connection conn;
	
	// session for user-initiated synchronous messages
	private Session clientSession;

	// session for listening and reacting to asynchronous messages
	private Session eventSession;
	
	// sender for the clientSession
	private MessageProducer clientSender;
	
	// sender for the eventSession
	private MessageProducer eventSender;

	// receiver of synchronous replies
	private MessageConsumer replyReceiver;
	
	// topic to send and receiver offers
	private Topic offerTopic;
	
	// queue for sending messages to bank
	private Queue toBankQueue;
	
	// queue for receiving synchronous replies
	private Queue replyQueue;

	// random number generator
	private Random rnd;
	
	// reader of lines from stdin
	private LineNumberReader in = new LineNumberReader(new InputStreamReader(System.in));
	
	/****	PRIVATE METHODS	****/
	
	/*
	 * Constructor, stores clientName, connection and initializes maps
	 */
	private Client(String clientName, Connection conn) {
		this.clientName = clientName;
		this.conn = conn;
		
		// initialize maps
		offeredGoods = new HashMap<String, Goods>();
		availableGoods = new HashMap<String, List<Goods>>();
		
		reservedGoods = new HashMap<String, Goods>();
		reserverAccounts = new HashMap<Integer, String>();
		reserverDestinations = new HashMap<String, Destination>();
		
		// generate some goods
		rnd = new Random();
		for (int i = 0; i < 10; i++) {
			addGoods();
		}
	}
	
	/*
	 * Generate a goods item
	 */
	private void addGoods() {
		String name = "";
		
		for (int i = 0; i < 4; i++) {
			char c = (char) ('A' + rnd.nextInt('Z' - 'A'));
			name += c;
		}
		
		offeredGoods.put(name, new Goods(name, rnd.nextInt(10000)));
	}
	
	/*
	 * Set up all JMS entities, get bank account, publish first goods offer 
	 */
	private void connect() throws JMSException {
        // create two sessions - one for synchronous and one for asynchronous processing
        clientSession = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
        eventSession = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
        
        // create (unbound) senders for the sessions
        clientSender = clientSession.createProducer(null);
        eventSender = eventSession.createProducer(null);
        
        // create queue for sending messages to bank
        toBankQueue = clientSession.createQueue(Bank.BANK_QUEUE);

        // create temporary queue for receiving first reply from bank
        Queue fromBankQueue = eventSession.createTemporaryQueue();
        // temporary receiver for the first reply from bank
        MessageConsumer tmpBankReceiver = clientSession.createConsumer(fromBankQueue);        
        
        // start processing messages
        conn.start();
        
        // request a bank account number
        Message msg = eventSession.createTextMessage(Bank.NEW_ACCOUNT_MSG);
        msg.setStringProperty(CLIENT_NAME_PROPERTY, clientName);
        // set ReplyTo that Bank will use to send me reply and later transfer reports
        msg.setJMSReplyTo(fromBankQueue);
        clientSender.send(toBankQueue, msg);
        
        // get reply from bank and store the account number
        TextMessage reply = (TextMessage) tmpBankReceiver.receive();
        accountNumber = Integer.parseInt(reply.getText());
        System.out.println("Account number: " + accountNumber);
        
        // close the temporary receiver
        tmpBankReceiver.close();
        
        // temporarily stop processing messages to finish initialization
        conn.stop();
        
        /* Processing bank reports */
        
        // create consumer of bank reports (from the fromBankQueue) on the event session
        MessageConsumer bankReceiver = eventSession.createConsumer(fromBankQueue);
        
        // set asynchronous listener for reports, using anonymous MessageListener
        // which just calls our designated method in its onMessage method
        bankReceiver.setMessageListener(new MessageListener() {
			@Override
			public void onMessage(Message msg) {
				try {
					processBankReport(msg);
				} catch (JMSException e) {
					e.printStackTrace();
				}
			}
        });
                
        // TODO finish the initialization
        
        /* Step 1: Processing offers */
        
        // create a topic both for publishing and receiving offers
        // hint: Sessions have a createTopic() method
        
        // create a consumer of offers from the topic using the event session
        
        // set asynchronous listener for offers (see above how it can be done)
        // which should call processOffer()
        
        /* Step 2: Processing sale requests */
        
        // create a queue for receiving sale requests (hint: Session has createQueue() method)
        // note that Session's createTemporaryQueue() is not usable here, the queue must have a name
        // that others will be able to determine from clientName (such as clientName + "SaleQueue")
                
        // create consumer of sale requests on the event session
                
        // set asynchronous listener for sale requests (see above how it can be done)
        // which should call processSale()
        
        // end TODO
        
        // create temporary queue for synchronous replies
        replyQueue = clientSession.createTemporaryQueue();
        
        // create synchronous receiver of the replies
        replyReceiver = clientSession.createConsumer(replyQueue);

        // restart message processing
        conn.start();
        
        // send list of offered goods
        publishGoodsList(clientSender);
    }

	/*
	 * Publish a list of offered goods
	 * Parameter is an (unbound) sender that fits into current session
	 * Sometimes we publish the list on user's request, sometimes we react to an event
	 */
	private void publishGoodsList(MessageProducer sender) throws JMSException {
		// TODO
		
		// create a message (of appropriate type) holding the list of offered goods
		// which can be created like this: new ArrayList<Goods>(offeredGoods.values())
		
		// don't forget to include the clientName in the message so other clients know
		// who is sending the offer - see how connect() does it when sending message to bank
		
		// send the message using the sender passed as parameter 
	}
	
	/*
	 * Send empty offer and disconnect from the broker 
	 */
	private void disconnect() throws JMSException {
		// delete all offered goods
		offeredGoods.clear();
		
		// send the empty list to indicate client quit
		publishGoodsList(clientSender);
		
		// close the connection to broker
		conn.close();
	}
	
	/*
	 * Print known goods that are offered by other clients
	 */
	private void list() {
		System.out.println("Available goods (name: price):");
		// iterate over sellers
		for (String sellerName : availableGoods.keySet()) {
			System.out.println("From " + sellerName);
			// iterate over goods offered by a seller
			for (Goods g : availableGoods.get(sellerName)) {
				System.out.println("  " + g);
			}
		}
	}
	
	/*
	 * Main interactive user loop
	 */
	private void loop() throws IOException, JMSException {
		// first connect to broker and setup everything
		connect();
		
		loop:
		while (true) {
			System.out.println("\nAvailable commands (type and press enter):");
			System.out.println(" l - list available goods");
			System.out.println(" p - publish list of offered goods");
			System.out.println(" b - buy goods");
			System.out.println(" q - quit");
			// read first character
			int c = in.read();
			// throw away rest of the buffered line
			while (in.ready()) in.read();
			switch (c) {
				case 'q':
					disconnect();
					break loop;
				case 'b':
					buy();
					break;
				case 'l':
					list();
					break;
				case 'p':
					publishGoodsList(clientSender);
					System.out.println("List of offers published");
					break;
				case '\n':
				default:
					break;
			}
		}
	}
	
	/*
	 * Perform buying of goods
	 */
	private void buy() throws IOException, JMSException {
		// get information from the user
		System.out.println("Enter seller name:");
		String sellerName = in.readLine();
		System.out.println("Enter goods name:");
		String goodsName = in.readLine();

		// check if the seller exists
		List<Goods> sellerGoods = availableGoods.get(sellerName);
		if (sellerGoods == null) {
			System.out.println("Seller does not exist: " + sellerName);
			return;
		}
		
		// TODO
		
		// First consider what message types clients will use for communicating a sale
		// we will need to transfer multiple values (of String and int) in each message 
		// MapMessage? ObjectMessage? TextMessage with extra properties?
		
		/* Step 1: send a message to the seller requesting the goods */
		
		// create local reference to the seller's queue
		// similar to Step 2 in connect() but using sellerName instead of clientName
		
		// create message requesting sale of the goods
		// includes: clientName, goodsName, accountNumber
		// also include reply destination that the other client will use to send reply (replyQueue)
		// how? see how connect() uses SetJMSReplyTo() 
					
		// send the message (with clientSender)
		
		/* Step 2: get seller's response and process it */
		
		// receive the reply (synchronously, using replyReceiver)
		
		// parse the reply (depends on your selected message format)
		// distinguish between "sell denied" and "sell accepted" message
		// in case of "denied", report to user and return from this method
		// in case of "accepted"
		// - obtain seller's account number and price to pay
		int price = 0;
		int sellerAccount = 0;

		/* Step 3: send message to bank requesting money transfer */
		
		// create message ordering the bank to send money to seller
		MapMessage bankMsg = clientSession.createMapMessage();
		bankMsg.setStringProperty(CLIENT_NAME_PROPERTY, clientName);
		bankMsg.setInt(Bank.ORDER_TYPE_KEY, Bank.ORDER_TYPE_SEND);
		bankMsg.setInt(Bank.ORDER_RECEIVER_ACC_KEY, sellerAccount);
		bankMsg.setInt(Bank.AMOUNT_KEY, price);
		
		System.out.println("Sending $" + price + " to account " + sellerAccount);
		
		// send message to bank
		clientSender.send(toBankQueue, bankMsg);

		/* Step 4: wait for seller's sale confirmation */
		
		// receive the confirmation, similar to Step 2

		// parse message and verify it's confirmation message
		
		// report successful sale to the user
	}
	
	/*
	 * Process a message with goods offer
	 */
	private void processOffer(Message msg) throws JMSException {
		// TODO
		
		// parse the message, obtaining sender's name and list of offered goods
		
		// should ignore messages sent from myself
		// if (clientName.equals(sender)) ...
		
		// store the list into availableGoods (replacing any previous offer)
		// empty list means disconnecting client, remove it from availableGoods completely
//		if (lst.isEmpty()) {
//			availableGoods.remove(sender);
//		} else {
//			availableGoods.put(sender, lst);
//		}
	}
	
	/*
	 * Process message requesting a sale
	 */
	private void processSale(Message msg) throws JMSException {
		// TODO
		
		/* Step 1: parse the message */
		
		// distinguish that it's the sale request message

		// obtain buyer's name (buyerName), goods name (goodsName) , buyer's account number (buyerAccount)
		
		// also obtain reply destination (buyerDest)
		// how? see for example Bank.processTextMessage()

		/* Step 2: decide what to do and modify data structures accordingly */
		
		// check if we still offer this goods
//		Goods goods = offeredGoods.get(goodsName);
//		if (goods != null) ...

		// if yes, we should remove it from offeredGoods and publish new list
		// also it's useful to create a list of "reserved goods" together with buyer's information
		// such as name, account number, reply destination
//		offeredGoods.remove(goodsName);
//		reservedGoods.put(buyerName, goods);
//		reserverAccounts.put(buyerAccount, buyerName);
//		reserverDestinations.put(buyerName, buyerDest);
		
		/* Step 3: send reply message */
		
		// prepare reply message (accept or deny)
		// accept message includes: my account number (accountNumber), price (goods.price)
		
		// send reply
	}
	
	/*
	 * Process message with (transfer) report from the bank
	 */
	private void processBankReport(Message msg) throws JMSException {
		/* Step 1: parse the message */
		
		// Bank reports are sent as MapMessage
		if (msg instanceof MapMessage) {
			MapMessage mapMsg = (MapMessage) msg;
			// get report number
			int cmd = mapMsg.getInt(Bank.REPORT_TYPE_KEY);
			if (cmd == Bank.REPORT_TYPE_RECEIVED) {
				// get account number of sender and the amount of money sent
				int buyerAccount = mapMsg.getInt(Bank.REPORT_SENDER_ACC_KEY);
				int amount = mapMsg.getInt(Bank.AMOUNT_KEY);
				
				// match the sender account with sender
				String buyerName = reserverAccounts.get(buyerAccount);
				
				// match the reserved goods
				Goods g = reservedGoods.get(buyerName);
				
				System.out.println("Received $" + amount + " from " + buyerName);
				
				/* Step 2: decide what to do and modify data structures accordingly */
				
				// did he pay enough?
				if (amount >= g.price) {
					// get the buyer's destination
					Destination buyerDest = reserverDestinations.get(buyerName);

					// remove the reserved goods and buyer-related information
					reserverDestinations.remove(buyerName);
					reserverAccounts.remove(buyerAccount);
					reservedGoods.remove(buyerName);
					
					/* TODO Step 3: send confirmation message */

					// prepare sale confirmation message
					// includes: goods name (g.name)
					
					// send reply (destination is buyerDest)
				} else {
					// we don't consider this now for simplicity
				}
			} else {
				System.out.println("Received unknown MapMessage:\n: " + msg);
			}
		} else {
			System.out.println("Received unknown message:\n: " + msg);
		}		
	}
	
	/**** PUBLIC METHODS ****/
	
	/*
	 * Main method, creates client instance and runs its loop
	 */
	public static void main(String[] args) {

		if (args.length != 1) {
			System.err.println("Usage: ./client <clientName>");
			return;
		}
		
		Connection connection = null;
		
		Client client = null;
		
		try {
            // create connection to the broker.
            ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://localhost:61616");
            connection = connectionFactory.createConnection();
            
            // create instance of the client
            client = new Client(args[0], connection);
            
            // perform client loop
            client.loop();
		}
		catch (Exception e) {
			e.printStackTrace();
		} finally {
	        try {
	            connection.close();
	        } catch (Throwable ignore) {
	        }
		}
	}
}
