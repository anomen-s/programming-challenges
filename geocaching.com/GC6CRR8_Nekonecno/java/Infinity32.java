public class Infinity32
{

    public static final String INF = "INFINITY";

    public static final String START = "01000011000001010000000000000000";


    public static String leftPadFloat(long lVal) 
    {
        StringBuilder res = new StringBuilder(Long.toBinaryString(lVal));
        while (res.length() < 32) {
          res.insert(0, '0');
        }
        return res.toString();
    }


    public static String encode(float f)
    {
            long lVal = Float.floatToIntBits(f);
            return leftPadFloat(lVal);
       
    }

    public static double decode(String s)
    {
        final int intVal = Integer.parseInt(s, 2);
        float floatVal = Float.intBitsToFloat(intVal);
        return floatVal;
    }
    
    public static String next(String current)
    {

        final int intVal = Integer.parseInt(current, 2);
        float floatVal = Float.intBitsToFloat(intVal);
	System.out.println("DEBUG: param: " + intVal);
        if (intVal == Float.POSITIVE_INFINITY) {
            return INF;
        }

        float nextFloat = floatVal + 1.0f;
        if (nextFloat > floatVal) {
            int iVal = Float.floatToRawIntBits(nextFloat);
            return leftPadFloat(iVal);
        }

        else {
            return leftPadFloat(intVal + 1);
        }


    }



  public static void main(String[] argv) 
  {
     System.out.println(encode(8888880128f));
     System.out.println(encode(8888880129f));
     System.out.println(encode(8888888888.0f));
     System.out.println(encode(1.0f));
//     System.out.println(encode(5.0));
     System.out.println(encode(133.0f));
     System.out.println(next(START));

     System.out.println(decode("0" +"11101111" + "11111111111111111111110"));
     System.out.println(decode("0" +"11101111" + "11111111111111111111111"));
     System.out.println(decode("0" +"11110000" + "00000000000000000000000"));

  }
  
}
