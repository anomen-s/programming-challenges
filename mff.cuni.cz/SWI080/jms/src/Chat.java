import java.net.InetAddress;

import java.awt.Panel;
import java.awt.Dialog;
import java.awt.Frame;
import java.awt.Label;
import java.awt.Menu;
import java.awt.MenuBar;
import java.awt.MenuItem;
import java.awt.Button;
import java.awt.TextArea;
import java.awt.TextField;
import java.awt.Choice;
import java.awt.BorderLayout;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

import javax.jms.MessageListener;
import javax.jms.Connection;
import javax.jms.Session;
import javax.jms.MessageProducer;
import javax.jms.MessageConsumer;
import javax.jms.Topic;
import javax.jms.Message;
import javax.jms.TextMessage;
import javax.jms.ObjectMessage;
import javax.jms.MapMessage;
import javax.jms.BytesMessage;
import javax.jms.StreamMessage;
import javax.jms.DeliveryMode;

import org.apache.activemq.ActiveMQConnectionFactory;

/**
 * The Chat example is a basic 'chat' application that uses
 * the JMS APIs. It uses JMS Topics to represent chat rooms or 
 * chat topics.
 *
 * When the application is launched, use the 'Chat' menu to
 * start or connect to a chat session.
 *
 * It should be pointed out that the bulk of the application is
 * AWT -- code for the GUI. The code that implements the messages
 * sent/received by the chat application is small in size.
 *
 * The Chat example consists of the following classes, all
 * contained in one file:
 *
 *  Chat           - Contains main() entry point, GUI/JMS initialization code.
 *  ChatPanel      - GUI for message textareas.
 *  ChatDialog     - GUI for "Connect" popup dialog.
 *  ChatObjMessage - Chat message class.
 *
 * Description of the ChatObjMessage class and how it is used
 * ==========================================================
 * The ChatObjMessage class is used to broadcast messages in
 * the JMS Chat example. 
 * The interface ChatMessageTypes (defined in this file) has
 * several message 'types':
 *  
 * From the interface definition:
 *  public static int JOIN  = 0;
 *  public static int MSG   = 1;
 *  public static int LEAVE = 2;
 *  
 * JOIN  - For applications to announce that they just joined the chat.
 * MSG   - For normal text messages.
 * LEAVE - For applications to announce that are leaving the chat.
 *  
 * Each ChatObjMessage also has fields to indicate who the sender is
 * (a plain String identifier).
 *  
 * When the chat application enters a chat session, it broadcasts a JOIN
 * message. Everybody currently in the chat session will get this and
 * the chat GUI will recognize the message of type JOIN and will print
 * something like this in the 'Messages in chat:' textarea:
 *  
 *  *** Anonymous has joined chat session
 *  
 * Once an application has entered a chat session, messages sent as part of
 * a normal 'chat' are sent as ChatObjMessage's of type MSG. Upon seeing
 * these messages, the chat GUI simply displays the sender and the message
 * text as follows:
 *  
 *  Anonymous: Hello World!
 *  
 * When a chat disconnect is done, prior to doing the various JMS cleanup
 * operations, a LEAVE message is sent. The chat GUI sees this and prints
 * something like:
 *  
 *  *** Anonymous has left chat session
 * 
 */

public class Chat implements ActionListener, WindowListener, MessageListener {
	String userName;
	String topicName;
	String hostName;
	
	ChatMessageCreator txtMsgCreator = null;
	ChatMessageCreator objMsgCreator = null;
	ChatMessageCreator mapMsgCreator = null;
	ChatMessageCreator bytesMsgCreator = null;
	ChatMessageCreator streamMsgCreator = null;
	
	ChatPanel panel;
	ChatDialog dialog = null;
	
	int outgoingMsgType;
	String outgoingMsgTypeString;
	ChatMessageCreator outgoingMsgCreator;
	
	ActiveMQConnectionFactory connectionFactory;
	Connection connection;
	Session session;
	MessageProducer msgProducer;
	MessageConsumer msgConsumer;
	Topic topic;

	boolean connected = false;
	
	Frame frame;
	MenuItem connectItem;
	MenuItem disconnectItem;
	MenuItem clearItem;
	MenuItem exitItem;
	Button sendBtn;
	Button connectBtn;
	Button cancelBtn;

	public static void main(String[] args) {
		Chat chat = new Chat();
		chat.initGUI();
		chat.initJMS();
	}

	/**
	 * Chat constructor.
	 * Initializes the chat user name, topic, hostname.
	 */
	public Chat() {
		userName = System.getProperty("user.name", "Anonymous");
		topicName = "Default";
		
		try {
			hostName = InetAddress.getLocalHost().getHostName();
		} catch (Exception e) {
			hostName = "localhost";
		}
	}

	public ChatMessageCreator getMessageCreator(int type) {
		switch (type) {
			case ChatDialog.MSG_TYPE_TEXT:
				if (txtMsgCreator == null)
					txtMsgCreator = new ChatTextMessageCreator();
				return txtMsgCreator;
			case ChatDialog.MSG_TYPE_OBJECT:
				if (objMsgCreator == null)
					objMsgCreator = new ChatObjMessageCreator();
				return objMsgCreator;
			case ChatDialog.MSG_TYPE_MAP:
				if (mapMsgCreator == null)
					mapMsgCreator = new ChatMapMessageCreator();
				return mapMsgCreator;
			case ChatDialog.MSG_TYPE_BYTES:
				if (bytesMsgCreator == null)
					bytesMsgCreator = new ChatBytesMessageCreator();
				return bytesMsgCreator;
			case ChatDialog.MSG_TYPE_STREAM:
				if (streamMsgCreator == null)
					streamMsgCreator = new ChatStreamMessageCreator();
				return streamMsgCreator;
		}
		
		return null;
	}
	
	public ChatMessageCreator getMessageCreator(Message msg) {
		if (msg instanceof TextMessage) {
			if (txtMsgCreator == null)
				txtMsgCreator = new ChatTextMessageCreator();
			return txtMsgCreator;
		} else if (msg instanceof ObjectMessage) {
			if (objMsgCreator == null)
				objMsgCreator = new ChatObjMessageCreator();
			return objMsgCreator;
		} else if (msg instanceof MapMessage) {
			if (mapMsgCreator == null)
				mapMsgCreator = new ChatMapMessageCreator();
			return mapMsgCreator;
		} else if (msg instanceof BytesMessage) {
			if (bytesMsgCreator == null)
				bytesMsgCreator = new ChatBytesMessageCreator();
			return bytesMsgCreator;
		} else if (msg instanceof StreamMessage) {
			if (streamMsgCreator == null)
				streamMsgCreator = new ChatStreamMessageCreator();
			return streamMsgCreator;
		}
		
		return null;
	}
	
	/* ActionListener */

	/**
	 * Detects the various GUI actions and performs the relevant action:
	 *
	 *  Connect menu item (on Chat menu)    - Show Connect dialog.
	 *  Disconnect menu item (on Chat menu) - Disconnect from chat.
	 *  Connect button (on Connect dialog)  - Connect to specified chat.
	 *  Cancel button (on Connect dialog)   - Hide Connect dialog.
	 *  Send button                         - Send message to chat
	 *  Clear menu item (on Chat menu)      - Clear chat textarea
	 *  Exit menu item (on Chat menu)       - Exit application
	 *
	 * @param ActionEvent GUI event
	 *
	 */
	public void actionPerformed(ActionEvent e) {
		Object obj = e.getSource();
		
		if (obj == connectItem)
			queryForChatNames();
		else if (obj == disconnectItem)
			doDisconnect();
		else if (obj == connectBtn) {
			dialog.setVisible(false);
			
			topicName = dialog.getChatTopicName();
			userName = dialog.getChatUserName();
			outgoingMsgTypeString = dialog.getMsgTypeString();
			outgoingMsgType = dialog.getMsgType();
			
			doConnect();
		} else if (obj == cancelBtn)
			dialog.setVisible(false);
		else if (obj == sendBtn)
			sendNormalMessage();
		else if (obj == clearItem)
			panel.clear();
		else if (obj == exitItem)
			exit();
	}
	
	/* WindowListener */
	
	public void windowClosing(WindowEvent e) {
		e.getWindow().dispose();
	}
	
	public void windowClosed(WindowEvent e) {
		exit();
	}
	
	public void windowActivated(WindowEvent e) { 
	}
	
	public void windowDeactivated(WindowEvent e) {
	}
	
	public void windowDeiconified(WindowEvent e) {
	}
	
	public void windowIconified(WindowEvent e) {
	}
	
	public void windowOpened(WindowEvent e) {
	}
	
	/* MessageListener */
	
	/**
	 * Display chat message on GUI.
	 *
	 * @param msg Message received
	 *
	 */
	public void onMessage(Message msg) {
		ChatMessageCreator inboundMsgCreator = getMessageCreator(msg);
		
		if (inboundMsgCreator == null) {
			errorMessage("Message received is not supported!");
			return;
		}
		
		/* Need to fetch msg values in this order. */
		int type = inboundMsgCreator.getChatMessageType(msg);
		String sender = inboundMsgCreator.getChatMessageSender(msg);
		String msgText = inboundMsgCreator.getChatMessageText(msg);
		
		if (type == ChatMessageTypes.BADTYPE) {
			errorMessage("Message received in wrong format!");
			return;
		}
		
		panel.newMessage(sender, type, msgText);
	}

	/**
	 * Popup the ChatDialog to query the user for the chat user
	 * name and chat topic.
	 */
	private void queryForChatNames() {
		if (dialog == null) {
			dialog = new ChatDialog(frame);
			
			connectBtn = dialog.getConnectButton();
			connectBtn.addActionListener(this);
			
			cancelBtn = dialog.getCancelButton();
			cancelBtn.addActionListener(this);
		}
		
		dialog.setChatUserName(userName);
		dialog.setChatTopicName(topicName);
		dialog.setVisible(true);
	}

	/**
	 * Performs the actual chat connect.
	 * The createChatSession() method does the real work here, creating
	 * connection, session, topic, consumer and producer.
	 */
	private void doConnect() {
		if (connected)
			return;
		
		outgoingMsgCreator = getMessageCreator(outgoingMsgType);
		
		if (createChatSession(topicName) == false) {
			errorMessage("Unable to create Chat session. Please verify a broker is running.");
			return;
		}
		
		connectItem.setEnabled(false);
		disconnectItem.setEnabled(true);
		
		panel.setUserName(userName);
		panel.setDestName(topicName);
		panel.setMsgType(outgoingMsgTypeString);
		panel.setHostName(hostName);
		panel.setEnabled(true);
		
		connected = true;
	}

	/**
	 * Disconnects from chat session.
	 * destroyChatSession() performs the JMS cleanup.
	 */
	private void doDisconnect() {
		if (!connected)
			return;
		destroyChatSession();
		
		connectItem.setEnabled(true);
		disconnectItem.setEnabled(false);
		panel.setEnabled(false);
		
		connected = false;
	}

	/**
	 * Exit application.
	 * Does some cleanup if necessary.
	 */
	private void exit() {
		doDisconnect();
		System.exit(0);
	}

	/**
	 * Create the application GUI.
	 */
	private void initGUI() {
		frame = new Frame("Chat");
		frame.addWindowListener(this);
		
		MenuBar menubar = createMenuBar();
		frame.setMenuBar(menubar);
		
		panel = new ChatPanel();
		panel.setUserName(userName);
		panel.setDestName(topicName);
		panel.setHostName(hostName);
		
		sendBtn = panel.getSendButton();
		sendBtn.addActionListener(this);
		
		frame.add(panel);
		frame.pack();
		frame.setVisible(true);
		
		panel.setEnabled(false);
	}

	/**
	 * Create menubar for application.
	 */
	private MenuBar createMenuBar() {
		MenuBar bar = new MenuBar();
		
		Menu chatMenu = (Menu) bar.add(new Menu("Chat"));
		connectItem = (MenuItem) chatMenu.add(new MenuItem("Connect ..."));
		disconnectItem = (MenuItem) chatMenu.add(new MenuItem("Disconnect"));
		clearItem = (MenuItem) chatMenu.add(new MenuItem("Clear Messages"));
		exitItem = (MenuItem) chatMenu.add(new MenuItem("Exit"));
		
		disconnectItem.setEnabled(false);
		
		connectItem.addActionListener(this);
		disconnectItem.addActionListener(this);
		clearItem.addActionListener(this);
		exitItem.addActionListener(this);
		
		return bar;
	}

	/**
	 * Send message using text that is currently in the ChatPanel
	 * object. The text message is obtained via panel.getMessage()
	 *
	 * An object of type ChatObjMessage is created containing the typed
	 * text. A JMS ObjectMessage is used to encapsulate this ChatObjMessage
	 * object.
	 */
	private void sendNormalMessage() {
		if (!connected) {
			errorMessage("Cannot send message, not connected to chat session!");
			return;
		}
		
		try {
			Message msg = outgoingMsgCreator.createChatMessage(session, userName, ChatMessageTypes.NORMAL, panel.getMessage());
			msgProducer.send(msg);
			panel.setMessage("");
			panel.requestFocus();
		} catch (Exception e) {
			errorMessage("Caught exception while sending NORMAL message: " + e);
		}
	}

	/**
	 * Send a message to the chat session to inform people
	 * we just joined the chat.
	 */
	private void sendJoinMessage() {
		try {
			Message msg = outgoingMsgCreator.createChatMessage(session, userName, ChatMessageTypes.JOIN, null);
			msgProducer.send(msg);
		} catch (Exception e) {
			errorMessage("Caught exception while sending JOIN message: " + e);
		}
	}
	
	/**
	 * Send a message to the chat session to inform people
	 * we are leaving the chat.
	 */
	private void sendLeaveMessage() {
		try {
			Message msg = outgoingMsgCreator.createChatMessage(session, userName, ChatMessageTypes.LEAVE, null);
			msgProducer.send(msg);
		} catch (Exception e) {
			errorMessage("Caught exception while sending LEAVE message: " + e);
		}
	}

	/**
	 * JMS initialization.
	 * This is simply creating the ConnectionFactory.
	 */
	private void initJMS() {
		try {
			/* Note that the factory is usually obtained from JNDI, this method is ActiveMQ-specific
			   (used here for simplicity) */
			connectionFactory = new ActiveMQConnectionFactory("tcp://localhost:61616");
		} catch (Exception e) {
			errorMessage("Caught Exception: " + e);
		}
	}

	/**
	 * Create 'chat session'. This involves creating connection,
	 * session, topic, consumer and producer.
	 */
	private boolean createChatSession(String topicStr) {
		try {
			connection = connectionFactory.createConnection();
			session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
			topic = session.createTopic(topicStr);
			
			msgProducer = session.createProducer(topic);
			msgProducer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
			
			msgConsumer = session.createConsumer(topic);
			msgConsumer.setMessageListener(this);
			
			connection.start();
			sendJoinMessage();
			return true;
		} catch (Exception e) {
			errorMessage("Caught Exception: " + e);
			e.printStackTrace();
			return false; 
		}
	}
	
	/**
	 * Destroy/close 'chat session'.
	 */
	private void destroyChatSession() {
		try {
			sendLeaveMessage();
			
			msgConsumer.close();
			msgProducer.close();
			session.close();
			connection.close();
			
			topic = null;
			msgConsumer = null;
			msgProducer = null;
			session = null;
			connection = null;
		} catch (Exception e) {
			errorMessage("Caught Exception: " + e);
		}
	}

	/**
	 * Display error. Right now all we do is dump to
	 * stderr.
	 */
	private void errorMessage(String s) {
		System.err.println(s);
	}
}

/**
 * This class provides the bulk of the GUI:
 *  sendMsgTA - TextArea for typing messages to send
 *  msgsTA    - TextArea for displaying messages in chat
 *  sendBtn   - Send button for activating a message 'Send'
 *
 *  Plus various labels to indicate the chat topic name,
 *  the user name and host name.
 *
 */
class ChatPanel extends Panel implements ChatMessageTypes {
	private String destName;
	private String userName;
	private String msgType;
	private String hostName;
	
	private Label destLabel;
	private Label userLabel;
	private Label msgTypeLabel;
	private Label msgsLabel;
	private Label sendMsgLabel;
	
	private Button sendBtn;
	
	private TextArea sendMsgTA;
	private TextArea msgsTA;

	/**
	 * ChatPanel constructor.
	 */
	public ChatPanel() {
		init();
	}

	/**
	 * Set the chat username.
	 * @param userName Chat userName
	 */
	public void setUserName(String userName) {
		this.userName = userName;
		userLabel.setText("User Name: " + userName);
		sendBtn.setLabel("Send Message as " + userName);
	}
	
	/**
	 * Set the chat hostname. This is pretty much
	 * the host that the router is running on.
	 * @param hostName Chat hostName
	 */
	public void setHostName(String hostName) {
		this.hostName = hostName;
	}
	
	/**
	 * Set the topic name.
	 * @param destName Chat topic name
	 */
	public void setDestName(String destName) {
		this.destName = destName;
		destLabel.setText("Topic: " + destName);
	}

	public void setMsgType(String msgType) {
		this.msgType = msgType;
		msgTypeLabel.setText("Outgoing Message Type: " + msgType);
	}

	/**
	 * Return the 'Send' button.
	 */
	public Button getSendButton() {
		return sendBtn;
	}

	/**
	 * Clear the chat message text area.
	 */
	public void clear() {
		msgsTA.setText("");
	}

	/**
	 * Append the passed message to the chat message text area.
	 * @param msg Message to display
	 */
	public void newMessage(String sender, int type, String text) {
		switch (type) {
			case NORMAL:
				msgsTA.append(sender +  ": " + text + "\n");
				break;
			case JOIN:
				msgsTA.append("*** " +  sender +  " has joined chat session ***\n");
				break;
			case LEAVE:
				msgsTA.append("*** " +  sender +  " has left chat session ***\n");
				break;
		}
	}

	/**
	 * Set the string to display on the chat message textarea
	 * @param s String to display
	 */
	public void setMessage(String s) {
		sendMsgTA.setText(s);
	}
	
	/**
	 * Returns the contents of the chat message textarea
	 */
	public String getMessage() {
		return sendMsgTA.getText();
	}

	/*
	 * Init chat panel GUI elements.
	 */
	private void init() {
		setLayout(new BorderLayout(0, 0));
		destLabel = new Label("Topic:");
		userLabel = new Label("User Name:");
		msgTypeLabel = new Label("Outgoing Message Type:");
		
		Panel dummyPanel = new Panel();
		dummyPanel.setLayout(new BorderLayout(0, 0));
		dummyPanel.add("North", destLabel);
		dummyPanel.add("Center", userLabel);
		dummyPanel.add("South", msgTypeLabel);
		add("North", dummyPanel);
		
		dummyPanel = new Panel();
		dummyPanel.setLayout(new BorderLayout(0, 0));
		msgsLabel = new Label("Messages in Chat:");
		msgsTA = new TextArea(15, 40);
		msgsTA.setEditable(false);
		
		dummyPanel.add("North", msgsLabel);
		dummyPanel.add("Center", msgsTA);
		add("Center", dummyPanel);
		
		dummyPanel = new Panel();
		dummyPanel.setLayout(new BorderLayout(0, 0));
		sendMsgLabel = new Label("Type Message:");
		sendMsgTA = new TextArea(5, 40);
		sendBtn = new Button("Send Message");
		dummyPanel.add("North", sendMsgLabel);
		dummyPanel.add("Center", sendMsgTA);
		dummyPanel.add("South", sendBtn);
		add("South", dummyPanel);
	}
}

/**
 * Dialog for querying the chat user name and chat topic.
 *
 */
class ChatDialog extends Dialog {
	
	public final static int MSG_TYPE_UNDEFINED = -1;
	public final static int MSG_TYPE_OBJECT = 0;
	public final static int MSG_TYPE_TEXT = 1;
	public final static int MSG_TYPE_MAP = 2;
	public final static int MSG_TYPE_BYTES = 3;
	public final static int MSG_TYPE_STREAM = 4;

	private TextField nameF;
	private TextField topicF;
	
	private Choice msgTypeChoice;
	private Button connectBtn;
	private Button cancelBtn;

	/**
	 * ChatDialog constructor.
	 * @param f Parent frame.
	 */
	public ChatDialog(Frame f) {
		super(f, "Chat: Connect Information", true);
		init();
		setResizable(false);
	}

	/**
	 * Return 'Connect' button
	 */
	public Button getConnectButton() {
		return connectBtn;
	}
	
	/**
	 * Return 'Cancel' button
	 */
	public Button getCancelButton() {
		return cancelBtn;
	}

	/**
	 * Return chat user name entered.
	 */
	public String getChatUserName() {
		if (nameF == null)
			return null;
		return nameF.getText();
	}
	
	/**
	 * Set chat user name.
	 * @param s chat user name
	 */
	public void setChatUserName(String s) {
		if (nameF != null)
			nameF.setText(s);
	}

	/**
	 * Set chat topic
	 * @param s chat topic
	 */
	public void setChatTopicName(String s) {
		if (topicF != null)
			topicF.setText(s);
	}
	
	/**
	 * Return chat topic
	 */
	public String getChatTopicName() {
		if (topicF == null)
	  		return null;
		return topicF.getText();
	}

	/*
	 * Get message type
	 */
	public int getMsgType() {
		if (msgTypeChoice == null)
			return MSG_TYPE_UNDEFINED;
		return msgTypeChoice.getSelectedIndex();
	}

	public String getMsgTypeString() {
		if (msgTypeChoice == null)
			return null;
		return msgTypeChoice.getSelectedItem();
	}

	/*
	 * Init GUI elements.
	 */
	private void init() {
		Panel panel = new Panel();
		panel.setLayout(new BorderLayout());
		
		Panel dummyPanel = new Panel();
		dummyPanel.setLayout(new BorderLayout());
		
		Panel labelPanel = new Panel();
		GridBagLayout labelGbag = new GridBagLayout();
		GridBagConstraints labelConstraints = new GridBagConstraints();
		labelPanel.setLayout(labelGbag);
		int j = 0;
		
		Panel valuePanel = new Panel();
		GridBagLayout valueGbag = new GridBagLayout();
		GridBagConstraints valueConstraints = new GridBagConstraints();
		valuePanel.setLayout(valueGbag);
		int i = 0;
		
		Label chatNameLabel = new Label("Chat User Name:", Label.RIGHT);
		Label chatTopicLabel = new Label("Chat Topic:", Label.RIGHT);
		Label msgTypeLabel = new Label("Outgoing Msg Type:", Label.RIGHT);
		
		labelConstraints.gridx = 0;
		labelConstraints.gridy = j++;
		labelConstraints.weightx = 1.0;
		labelConstraints.weighty = 1.0;
		labelConstraints.anchor = GridBagConstraints.EAST;
		labelGbag.setConstraints(chatNameLabel, labelConstraints);
		labelPanel.add(chatNameLabel);
		
		labelConstraints.gridy = j++;
		labelGbag.setConstraints(chatTopicLabel, labelConstraints);
		labelPanel.add(chatTopicLabel);
		
		labelConstraints.gridy = j++;
		labelGbag.setConstraints(msgTypeLabel, labelConstraints);
		labelPanel.add(msgTypeLabel);
		
		nameF = new TextField(20);
		topicF = new TextField(20);
		msgTypeChoice = new Choice();
		msgTypeChoice.insert("ObjectMessage", MSG_TYPE_OBJECT);
		msgTypeChoice.insert("TextMessage", MSG_TYPE_TEXT);
		msgTypeChoice.insert("MapMessage", MSG_TYPE_MAP);
		msgTypeChoice.insert("BytesMessage", MSG_TYPE_BYTES);
		msgTypeChoice.insert("StreamMessage", MSG_TYPE_STREAM);
		msgTypeChoice.select(MSG_TYPE_STREAM);
		
		valueConstraints.gridx = 0;
		valueConstraints.gridy = i++;
		valueConstraints.weightx = 1.0;
		valueConstraints.weighty = 1.0;
		valueConstraints.anchor = GridBagConstraints.WEST;
		valueGbag.setConstraints(nameF, valueConstraints);
		valuePanel.add(nameF);
		
		valueConstraints.gridy = i++;
		valueGbag.setConstraints(topicF, valueConstraints);
		valuePanel.add(topicF);
		
		valueConstraints.gridy = i++;
		valueGbag.setConstraints(msgTypeChoice, valueConstraints);
		valuePanel.add(msgTypeChoice);
		
		dummyPanel.add("West", labelPanel);
		dummyPanel.add("Center", valuePanel);
		
		panel.add("North", dummyPanel);
		
		dummyPanel = new Panel();
		connectBtn = new Button("Connect");
		cancelBtn = new Button("Cancel");
		dummyPanel.add(connectBtn);
		dummyPanel.add(cancelBtn);
		
		panel.add("South", dummyPanel);
		add(panel);
		pack();
	}
}

interface ChatMessageTypes {
	public static int JOIN = 0;
	public static int NORMAL = 1;
	public static int LEAVE = 2;
	public static int BADTYPE = -1;
}

interface ChatMessageCreator {
	public Message createChatMessage(Session session, String sender, int type, String text);
	public boolean isUsable(Message msg);
	public int getChatMessageType(Message msg);
	public String getChatMessageSender(Message msg);
	public String getChatMessageText(Message msg);
}

class ChatTextMessageCreator implements ChatMessageCreator, ChatMessageTypes {
	private static String MSG_SENDER_PROPNAME = "CHAT_MSG_SENDER";
	private static String MSG_TYPE_PROPNAME = "CHAT_MSG_TYPE";

	public Message createChatMessage(Session session, String sender, int type, String text) {
		TextMessage txtMsg = null;
		
		try {
			txtMsg = session.createTextMessage();
			txtMsg.setStringProperty(MSG_SENDER_PROPNAME, sender);
			txtMsg.setIntProperty(MSG_TYPE_PROPNAME, type);
			txtMsg.setText(text);
		} catch (Exception e) {
			System.err.println("Caught exception while creating message: " + e);
		}
		
		return txtMsg;
	}

	public boolean isUsable(Message msg) {
		if (msg instanceof TextMessage)
			return true;
		return false;
	}

	public int getChatMessageType(Message msg) {
		int type = BADTYPE;
		
		try {
			TextMessage txtMsg = (TextMessage) msg;
			type = txtMsg.getIntProperty(MSG_TYPE_PROPNAME);
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return type;
	}

	public String getChatMessageSender(Message msg) {
		String sender = null;
		
		try {
			TextMessage txtMsg = (TextMessage) msg;
			sender = txtMsg.getStringProperty(MSG_SENDER_PROPNAME);
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return sender;
	}

	public String getChatMessageText(Message msg) {
		String text = null;
		
		try {
			TextMessage txtMsg = (TextMessage) msg;
			text = txtMsg.getText();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return text;
	}
}

class ChatObjMessageCreator implements ChatMessageCreator, ChatMessageTypes {
	public Message createChatMessage(Session session, String sender, int type, String text) {
		ObjectMessage objMsg = null;
		ChatObjMessage sMsg;
		
		try {
			objMsg = session.createObjectMessage();
			sMsg = new ChatObjMessage(sender, type, text);
			objMsg.setObject(sMsg);
		} catch (Exception e) {
			System.err.println("Caught exception while creating message: " + e);
		}
		
		return objMsg;
	}

	public boolean isUsable(Message msg) {
		try {
			ChatObjMessage sMsg = getChatMessage(msg);
			if (sMsg == null)
				return false;
			
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
			return false;
		}
		
		return true;
	}

	public int getChatMessageType(Message msg) {
		int type = BADTYPE;
		
		try {
			ChatObjMessage sMsg = getChatMessage(msg);
			if (sMsg != null)
				type = sMsg.getType();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return type;
	}

	public String getChatMessageSender(Message msg) {
		String sender = null;
		
		try {
			ChatObjMessage sMsg = getChatMessage(msg);
			if (sMsg != null)
				sender = sMsg.getSender();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return sender;
	}

	public String getChatMessageText(Message msg) {
		String text = null;
		
		try {
			ChatObjMessage sMsg = getChatMessage(msg);
			if (sMsg != null)
				text = sMsg.getMessage();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return text;
	}

	private ChatObjMessage getChatMessage(Message msg) {
		ObjectMessage objMsg;
		ChatObjMessage sMsg = null;
		
		if (!(msg instanceof ObjectMessage)) {
			System.err.println("Message received not of type ObjectMessage!");
			return null;
		}
		
		objMsg = (ObjectMessage) msg;
		
		try {
			sMsg = (ChatObjMessage) objMsg.getObject();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return sMsg;
	}
}

class ChatMapMessageCreator implements ChatMessageCreator, ChatMessageTypes {
	private static String MAPMSG_SENDER_PROPNAME = "CHAT_MAPMSG_SENDER";
	private static String MAPMSG_TYPE_PROPNAME = "CHAT_MAPMSG_TYPE";
	private static String MAPMSG_TEXT_PROPNAME = "CHAT_MAPMSG_TEXT";

	public Message createChatMessage(Session session, String sender, int type, String text) {
		MapMessage mapMsg = null;
		
		try {
			mapMsg = session.createMapMessage();
			mapMsg.setInt(MAPMSG_TYPE_PROPNAME, type);
			mapMsg.setString(MAPMSG_SENDER_PROPNAME, sender);
			mapMsg.setString(MAPMSG_TEXT_PROPNAME, text);
		} catch (Exception e) {
			System.err.println("Caught exception while creating message: " + e);
		}
		
		return mapMsg;
	}

	public boolean isUsable(Message msg) {
		if (msg instanceof MapMessage)
			return true;
		return false;
	}

	public int getChatMessageType(Message msg) {
		int type = BADTYPE;
		
		try {
			MapMessage mapMsg = (MapMessage) msg;
			type = mapMsg.getInt(MAPMSG_TYPE_PROPNAME);
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return type;
	}

	public String getChatMessageSender(Message msg) {
		String sender = null;
		
		try {
			MapMessage mapMsg = (MapMessage) msg;
			sender = mapMsg.getString(MAPMSG_SENDER_PROPNAME);
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return sender;
	}

	public String getChatMessageText(Message msg) {
		String text = null;
		
		try {
			MapMessage mapMsg = (MapMessage) msg;
			text = mapMsg.getString(MAPMSG_TEXT_PROPNAME);
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return text;
	}
}

class ChatBytesMessageCreator implements ChatMessageCreator, ChatMessageTypes {
	public Message createChatMessage(Session session, String sender, int type, String text) {
		BytesMessage bytesMsg = null;
		
		try {
			byte data[];
			
			bytesMsg = session.createBytesMessage();
			bytesMsg.writeInt(type);
			
			/* Write length of sender and text strings */
			data = sender.getBytes();
			bytesMsg.writeInt(data.length);
			bytesMsg.writeBytes(data);
			
			if (text != null) {
				data = text.getBytes();
				bytesMsg.writeInt(data.length);
				bytesMsg.writeBytes(data);
			} else
				bytesMsg.writeInt(0);
		} catch (Exception e) {
			System.err.println("Caught exception while creating message: " + e);
		}
		
		return bytesMsg;
	}

	public boolean isUsable(Message msg) {
		if (msg instanceof BytesMessage)
			return true;
		return false;
	}

	public int getChatMessageType(Message msg) {
		int type = BADTYPE;
		
		try {
			BytesMessage bytesMsg = (BytesMessage) msg;
			type = bytesMsg.readInt();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return type;
	}

	public String getChatMessageSender(Message msg) {
		return readSizeFetchString(msg);
	}

	public String getChatMessageText(Message msg) {
		return readSizeFetchString(msg);
	}

	private String readSizeFetchString(Message msg) {
		String stringData = null;
		
		try {
			BytesMessage bytesMsg = (BytesMessage) msg;
			int length = bytesMsg.readInt();
			
			if (length == 0)
				return "";
			
			byte data[] = new byte[length];
			
			/* Loop to keep reading until all the bytes are read in */
			int left = length;
			while (left > 0) {
				byte tmpBuf[] = new byte[left];
				int ret = bytesMsg.readBytes(tmpBuf);
				if (ret > 0) {
					for (int i = 0; i < ret; ++i)
						data[data.length - left + i] = tmpBuf[i];
					left -= ret;
				}
			}
			
			stringData = new String(data);
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return stringData;
	}
}

class ChatStreamMessageCreator implements ChatMessageCreator, ChatMessageTypes {
	public Message createChatMessage(Session session, String sender, int type, String text) {
		StreamMessage streamMsg = null;
		
		try {
			byte data[];
			
			streamMsg = session.createStreamMessage();
			streamMsg.writeInt(type);
			streamMsg.writeString(sender);
			
			if (text == null)
				text = "";
			
			streamMsg.writeString(text);
		} catch (Exception e) {
			System.err.println("Caught exception while creating message: " + e);
		}
		
		return streamMsg;
	}

	public boolean isUsable(Message msg) {
		if (msg instanceof StreamMessage)
			return true;
		return false;
	}

	public int getChatMessageType(Message msg) {
		int type = BADTYPE;
		
		try {
			StreamMessage streamMsg = (StreamMessage) msg;
			type = streamMsg.readInt();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return type;
	}

	public String getChatMessageSender(Message msg) {
		String sender = null;
		
		try {
			StreamMessage streamMsg = (StreamMessage) msg;
			sender = streamMsg.readString();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return sender;
	}

	public String getChatMessageText(Message msg) {
		String text = null;
		
		try {
			StreamMessage streamMsg = (StreamMessage) msg;
			text = streamMsg.readString();
		} catch (Exception e) {
			System.err.println("Caught exception: " + e);
		}
		
		return text;
	}
}

/**
 * Object representing a message sent by chat application.
 * We use this class and wrap a javax.jms.ObjectMessage
 * around it instead of using a javax.jms.TextMessage
 * because a simple string is not sufficient. We want
 * be able to to indicate that a message is one of these 
 * types: JOIN, MSG, LEAVE
 *
 */
class ChatObjMessage implements java.io.Serializable, ChatMessageTypes {
	private int type = NORMAL;
	private String sender;
	private String message;
	
	/**
	 * ChatObjMessage constructor. Construct a message with the given
	 * sender and message.
	 * @param sender Message sender
	 * @param type Message type
	 * @param message The message to send
	 */
	public ChatObjMessage(String sender, int type, String message) {
		this.sender = sender;
		this.type = type;
		this.message = message;
	}

	/**
	 * Return message sender.
	 */
	public String getSender() {
		return sender;
	}

	/**
	 * Return message type.
	 */
	public int getType() {
		return type;
	}

	/**
	 * Sets the message string.
	 * @param message The message string
	 */
	public void setMessage(String message) {
		this.message = message;
	}
	
	/**
	 * Return the message string
	 */
	public String getMessage() {
		return message;
	}
}
