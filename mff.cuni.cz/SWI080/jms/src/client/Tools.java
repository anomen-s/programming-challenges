/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

// $Id: Tools.java 98 2009-04-15 12:04:14Z ludek $

package client;

import java.util.Collection;

/**
 *
 * @author ludek
 * @version $Rev: 98 $
 */
public class Tools {

    public static Goods findInList(Collection<Goods> list, String name)
    {
        for (Goods g: list)
        {
            if (name.equals(g.name))
                return g;
        }
        return null;
    }
}
