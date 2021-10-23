/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

// $Id: Consts.java 98 2009-04-15 12:04:14Z ludek $

package client;

/**
 *
 * @author ludek
 * @version $Rev: 98 $
 */
public interface Consts {
	/**** PUBLIC CONSTANTS - BANK ****/

	// text message command open new account
	public static final String NEW_ACCOUNT_MSG = "NEW_ACCOUNT";
	
	// MapMessage key for order type 
	//public static final String ORDER_TYPE_KEY = "orderType";

	// order type "send money"
	//public static final int ORDER_TYPE_SEND = 1;
	
	// MapMessage key for receiver's account number
	public static final String ORDER_RECEIVER_ACC_KEY = "receiverAccount";
	
	// MapMessage key for amount of money transfered 
	public static final String AMOUNT_KEY = "amount";
	
	// name of the queue for sending messages to Bank
	public static final String BANK_QUEUE = "BankQueue";

	// identifier of the queue for sending sal messages
      	public static final String SALE_QUEUE_TAG = "SaleQueue";

	// MapMessage key for report type
	//public static final String REPORT_TYPE_KEY = "reportType";
	 
	// report type "received money"
	//public static final int REPORT_TYPE_RECEIVED = 1;
	
	// MapMessage key for sender's account
	public static final String REPORT_SENDER_ACC_KEY = "senderAccount";

        public static final int START_CASH = 50000;

    	public static final String ACCOUNT_KEY = "account";
    	public static final String ACCOUNT_BALANCE_KEY = "balance";
        

        /****	CONSTANTS - CLIENT	****/
        // name of the property specifying client's name
        public static final String CLIENT_NAME_PROPERTY = "clientName";
        //public static final String OFFER_SENDER = "offerSender";
        
        public static final String GOODS_NAME = "goods_name";

        public static final String MSG_TYPE = "msg_type";

        public static final String MSG_TYPE_OFFER = "msg_offer";
        public static final String MSG_TYPE_OFFER_REQ = "msg_offer_req";

        public static final String MSG_TYPE_BALANCE_REQ = "msg_balance_req";
        public static final String MSG_TYPE_BALANCE = "msg_balance";
        
                
        public static final String MSG_TYPE_ORDER_SEND = "msg_order_send";
        public static final String MSG_TYPE_BUY = "msg_buy";
        public static final String MSG_TYPE_MONEY_RECVD = "msg_money_recvd";
        public static final String MSG_TYPE_NO_MONEY = "msg_no_money";
        
        public static final String MSG_TYPE_CONF = "msg_conf";
        public static final String MSG_TYPE_ACCEPT = "msg_accept";
        public static final String MSG_TYPE_DENY = "msg_deny";

        public static final String PRICE = "price";
        // name of the topic for publishing offers
        public static final String OFFER_TOPIC = "Offers";

}
