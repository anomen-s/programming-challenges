/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

// $Id: Account.java 98 2009-04-15 12:04:14Z ludek $

package client;

import javax.jms.Destination;

/**
 *
 * @author ludek
 * @version $Rev: 98 $
 */
public class Account {
	
        public final String name;
	
	public final int account;

        public int balance;
        
        public Destination destination;
        
//        public
                
        public Account(int account, String name) {
            this.account = account;
            this.name = name;
        }

        public Account(int account, String name, Destination destination) {
            this(account, name);
            this.destination = destination;
        }

        public Account(int account, String name, Destination destination, int balance) {
            this(account, name, destination);
            this.balance = balance;
        }

        public boolean withdraw(int value)
        {
            if (balance >= value) {
                balance -= value;
                return true;
            }
            return false;
        }
        
        public boolean insert(int value)
        {
            balance += value;
            return true;
        }
        

        @Override
        public String toString()
        {
            return "Account ["+name+","+account+","+balance+"]";
        }
                
                
}
