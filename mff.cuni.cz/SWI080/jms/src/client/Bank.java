package client;

// $Id$
import java.util.HashMap;
import java.util.Map;

import javax.jms.*;

import org.apache.activemq.ActiveMQConnectionFactory;

public class Bank implements MessageListener, Consts {

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
    private Map<String, Account> clientAccounts;
    // map client account numbers to client names
    private Map<Integer, Account> accountsClients;

    // map client names to client report destinations
    //private Map<String, Destination> clientDestinations;
    /**** PRIVATE METHODS ****/
    /*
     * Constructor, stores broker connection and initializes maps
     */
    private Bank(Connection conn)
    {
        this.conn = conn;

        // start with some arbitrary value
        lastAccount = 1000000;
        clientAccounts = new HashMap<String, Account>();
        accountsClients = new HashMap<Integer, Account>();
//		clientDestinations = new HashMap<String, Destination>();
    }

    /*
     * Initialize messaging structures, start listening for messages
     */
    private void init() throws JMSException
    {
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
    private void processTextMessage(TextMessage txtMsg) throws JMSException
    {
        // get the destination that client specified for replies
        // we will use it to send reply and also store it for transfer report messages
        Destination replyDest = txtMsg.getJMSReplyTo();
        // is it a NEW ACCOUNT message?
        if (NEW_ACCOUNT_MSG.equals(txtMsg.getText())) {
            // get the client's name stored as a property
            String clientName = txtMsg.getStringProperty(Client.CLIENT_NAME_PROPERTY);


            Account acc;
            // either assign new account number or return already known number
            if (clientAccounts.get(clientName) != null) {
                acc = clientAccounts.get(clientName);
                acc.destination = replyDest;
            } else {
                // also store the newly assigned number
                acc = new Account(lastAccount++, clientName, replyDest, START_CASH);
                clientAccounts.put(clientName, acc);
                accountsClients.put(acc.account, acc);
            }
            // store client's reply destination for future transfer reports


            System.out.println("Connected client " + clientName + " with account " + acc.account);

            // create reply TextMessage with the account number
            TextMessage reply = bankSession.createTextMessage(String.valueOf(acc.account));
            // send the reply to the provided reply destination
            bankSender.send(replyDest, reply);
        } else {
            System.out.println("Received unknown text message: " + txtMsg.getText());
            System.out.println("Full message info:\n" + txtMsg);
        }
    }

    /*
     * Handle map messages - in our case it's only the message ordering money transfer to a receiver account
     *
     * Also account balance queries
     */
    private void processMapMessage(MapMessage mapMsg) throws JMSException
    {

        // account balance queries
        if (MSG_TYPE_BALANCE_REQ.equals(mapMsg.getStringProperty(MSG_TYPE))) {
            int clientAccountNum = mapMsg.getInt(ACCOUNT_KEY);
            // find client's account number
            Account clientAccount = accountsClients.get(clientAccountNum);

            // create report message for the receiving client
            MapMessage reportMsg = bankSession.createMapMessage();

            // set sender's account number
            reportMsg.setInt(ACCOUNT_BALANCE_KEY, clientAccount.balance);
            reportMsg.setStringProperty(MSG_TYPE, MSG_TYPE_BALANCE);

            bankSender.send(clientAccount.destination, reportMsg);

        } else if (MSG_TYPE_ORDER_SEND.equals(mapMsg.getStringProperty(MSG_TYPE))) {
            // get client's name
            String clientName = mapMsg.getStringProperty(Client.CLIENT_NAME_PROPERTY);

            // find client's account number
            Account clientAccount = clientAccounts.get(clientName);

            // get receiver account number
            Account destAccount = accountsClients.get(mapMsg.getInt(ORDER_RECEIVER_ACC_KEY));

            // find receiving client's name
            //String destName = accountsClients.get(destAccount).name;

            // find receiving client's report message destination
            //Destination dest = accountsClients.get(destAccount.name).destination;

            // get amount of money being transferred
            int amount = mapMsg.getInt(AMOUNT_KEY);

            System.out.println("Transferring $" + amount + " from account " + clientAccount + " to account " + destAccount);

            // create report message for the receiving client
            MapMessage reportMsg = bankSession.createMapMessage();

            // set sender's account number
            reportMsg.setInt(REPORT_SENDER_ACC_KEY, clientAccount.account);

            // set money of amount transfered
            reportMsg.setInt(AMOUNT_KEY, amount);

            if (clientAccount.withdraw(amount)) {
                destAccount.insert(amount);
                // set report type to "you received money"
                reportMsg.setStringProperty(MSG_TYPE, MSG_TYPE_MONEY_RECVD);
            } else {
                reportMsg.setStringProperty(MSG_TYPE, MSG_TYPE_NO_MONEY);
            }

            // send report to receiver client's destination
            bankSender.send(destAccount.destination, reportMsg);

        } else {
            System.out.println("Received unknown MapMessage:\n" + mapMsg);
        }
    }

    /**** PUBLIC METHODS ****/
    /*
     * React to asynchronously received message
     */
    public void onMessage(Message msg)
    {
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
    public static void main(String[] args)
    {

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
        } catch (Exception e) {
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
