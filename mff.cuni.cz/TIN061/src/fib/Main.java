package fib;

import java.io.*;

/**
 * <p>Title: Fibonacci number system</p>
 * <p>Description: Main class</p>
 * <p>Copyright: Copyright (c) LH, 2004</p>
 * @author LH
 * @version 1.0
 */

public class Main {
  public Main()
  {

  }

  private static void print(FibNumber f1, FibNumber f2, FibNumber f3, String op)
  {
    System.out.print(f1);
    System.out.print(" " + op + " ");
    System.out.print(f2);
    System.out.print(" = ");
    System.out.print(f3);
    System.out.print(" (");
    System.out.print(f1.longValue());
    System.out.print(" " + op + " ");
    System.out.print(f2.longValue());
    System.out.print(" = ");
    System.out.print(f3.longValue());
    System.out.println(")");
  }

  public static void main(String[] argv)
  {
    FibNumber f1 = null;
    FibNumber f2 = null;
    if (argv.length == 0) {
//      System.out.println("Required arguments missing.");
//      return;
      argv = new String[] {"-i"};
    }

    if ("-sum".equalsIgnoreCase(argv[0])) {
      f1 = new FibNumber(argv[1]);
      f2 = new FibNumber(argv[2]);
      print(f1, f2, f1.add(f2), "+");
      print(f1, f2, f1.subtract(f2), "-");
      return;

    } else if ("-n".equalsIgnoreCase(argv[0])) {
      f1 = new FibNumber(Long.parseLong(argv[1]));
      f2 = new FibNumber(Long.parseLong(argv[2]));
      print(f1, f2, f1.add(f2), "+");
      print(f1, f2, f1.subtract(f2), "-");
      return;

    } else if ("-i".equalsIgnoreCase(argv[0])) {
      BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
      String num1 = null;
      String num2 = null;
      while (true) {
        try {
          System.out.print("Enter first number:  ");
          num1 = input.readLine();
          if ("".equals(num1)) {
            return;
          }
          f1 = new FibNumber(num1);
          System.out.print("Enter second number: ");
          num2 = input.readLine();
          if ("".equals(num2)) {
            return;
          }

          f2 = new FibNumber(num2);
        } //try
        catch (IOException ex) {}
        catch (NumberFormatException ex2) {
          System.out.println("Invalid number.");
          System.out.println("----------------------- (press Enter to exit)");
          continue;
        }
        print(f1, f2, f1.add(f2), "+");
        print(f1, f2, f1.subtract(f2), "-");
        System.out.println("---------------------- (press Enter to exit)");
      } //while
    } //elseif
  }

}