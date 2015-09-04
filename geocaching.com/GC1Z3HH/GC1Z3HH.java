public class GC1Z3HH {

  /*
     Vigenere cipher with known password
  */
  public static void main( String[] args ) {
      char[] encData = { 183, 164, 149, 171, 193, 146, 166, 186, 183, 166, 182, 188, 
       166, 166, 185, 172, 148, 171, 186, 150, 150, 189, 168, 164, 186, 179, 148, 166, 
       192, 181, 154, 169, 179, 165, 149, 187, 188, 163, 175, 156, 148, 166, 185, 177,
       146, 169, 194, 164, 166, 188, 179, 159, 187, 178, 167, 147, 170, 168, 165, 169,
       179, 157, 171, 170, 171, 165, 184, 183, 164, 166, 168, 182, 150, 170, 187, 149,
       151, 186, 164, 165, 186, 192, 154, 119 };
      char[] pass = "GC1FN12".toCharArray();
      for (int i = 0; i < encData.length; i++) {
         int E = encData[i];
         int K = pass[i % pass.length];
         //System.out.printf("\t%d\t%c\t%c\t%d\t%d\n", E, K, E-K, E ^ K, E & K);
         System.out.printf("%c", E-K);
     }
  }
}
