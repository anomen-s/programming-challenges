public class Infinity
{

    public static final String INF = "INFINITY";

    public static final String START = "0111111111110000000000000000000000000000000000000000000000000000";

    public static String leftPadFloat(long lVal) 
    {
        StringBuilder res = new StringBuilder(Long.toBinaryString(lVal));
        while (res.length() < 64) {
          res.insert(0, '0');
        }
        return res.toString();
    }

    public static String encode(double d)
    {
            long lVal = Double.doubleToRawLongBits(d);
            return leftPadFloat(lVal);
       
    }
    public static double decode(String s)
    {
        final long longVal = Long.parseLong(s, 2);
        double doubleVal = Double.longBitsToDouble(longVal);
        return doubleVal;
    }
    
    public static String next(String current)
    {

        final long longVal = Long.parseLong(current, 2);
        double doubleVal = Double.longBitsToDouble(longVal);
	System.out.println("DEBUG: param: " + doubleVal);
        if (doubleVal == Double.POSITIVE_INFINITY) {
            return INF;
        }

        double nextDouble = doubleVal + 1.0;
        if (nextDouble > doubleVal) {
            long lVal = Double.doubleToRawLongBits(nextDouble);
            return leftPadFloat(lVal);
        }

        else {
            return leftPadFloat(longVal + 1);
        }


    }



  public static void main(String[] argv) 
  {
     System.out.println(encode(5.0));
//     System.out.println(encode(5.0));
     System.out.println(encode(133.0));
     System.out.println(next(START));
  }
  
}
