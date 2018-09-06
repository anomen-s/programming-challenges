package fib;

import java.io.Serializable;
import java.util.Arrays;

/**
 * <p>Title: Fibonacci number system</p>
 * <p>Description: Arbitrary long integer represented in Fibonacci number system</p>
 * <p>Copyright: Copyright (c) LH, 2004</p>
 * @author Ludek Hlavacek
 * @version 1.0
 */

public class FibNumber
    extends Number implements Comparable, Serializable {

  public static final boolean PLUS = true;
  public static final boolean MINUS = false;

  private boolean sign = PLUS;

  /** Array representing number.<p>
   * <code>coef[i] == true </code> when number contains Fib(i),
   * where Fib(0) = 0, Fib(1) = 1, Fib(2) = 1, ...
   * </p><p>
   * Coefficients 0 and 1 are used internaly.
   * Normalized number has these two set to <code>false</code>.
   * Method toString starts printing with coefficient 2.
   * </p>
   */
  private boolean[] coef = new boolean[MARGIN];

  public FibNumber()
  {
    Arrays.fill(coef, false);
  }

  public FibNumber(long value)
  {
    setValue(value);
  }

  public FibNumber(String value) throws NumberFormatException
  {
    if ( (value == null) || (value.length() == 0) || (!setValue(value))) {
      throw new NumberFormatException();
    }
  }

  /** "copy-constructor" for internal use.
   * @param src source number
   */
  private FibNumber(FibNumber src)
  {
    sign = src.sign;
    coef = new boolean[src.coef.length];
    System.arraycopy(src.coef, 0, coef, 0, src.coef.length);
  }

  public double doubleValue()
  {
    double f = 0, f1 = 1, tmp, result = 0;
    for (int i = 0; i < coef.length; i++) {
      if (coef[i]) {
        result += f;
      }
      tmp = f;
      f += f1;
      f1 = tmp;
    } //for
    if (sign == MINUS) {
      return ( -result);
    }
    return result;
  }

  public float floatValue()
  {
    return (float) doubleValue();
  }

  public long longValue()
  {
    long f = 0, f1 = 1, tmp, result = 0;
    for (int i = 0; i < coef.length; i++) {
      if (coef[i]) {
        result += f;
      }
      tmp = f;
      f += f1;
      f1 = tmp;
    } //for
    if (sign == MINUS) {
      return ( -result);
    }
    return result;
  }

  public int intValue()
  {
    return (int) longValue();
  }

  public boolean equals(Object obj)
  {
    if (obj instanceof FibNumber) {
      return (compareTo( (FibNumber) obj) == 0);
    } //if
    return false;
  }

  public int hashCode()
  {
    long value = longValue();
    return (int) (value ^ (value >>> 32));
  }

  public String toString()
  {
    int l = digits();
    StringBuffer num = new StringBuffer(l);
    if (sign == MINUS) {
      num.append('-');
    }
    for (int i = l - 1; i > 1; i--) {
      if (coef[i]) {
        num.append('1');
      } else {
        num.append('0');
      }
    }
    if (num.length() == 0) {
      num.append("0");
    }
    return num.toString();
  }

  private int absCompare(FibNumber f2)
  {
    int d = digits(), d2 = f2.digits();
    if (d != d2) {
      return (d - d2);
    }
    for (int i = d - 1; i > 0; i--) {
      if (coef[i] != f2.coef[i]) {
        if (coef[i]) {
          return 1;
        } else {
          return -1;
        }
      }
    } //for
    return 0;
  }

  public int compareTo(FibNumber f2)
  {
    int result = 1;
    if (sign == MINUS) {
      result = -1;
    }
    if (sign != f2.sign) {
      return result;
    } //if
    return (result * absCompare(f2));
  }

  /** Compares this object with the specified object for order.
   * Returns a negative integer, zero, or a positive integer as this object is less than, equal to, or greater than the specified object.
   * @param o  the Object to be compared.
   * @return a negative integer, zero, or a positive integer as this object is less than, equal to, or greater than the specified object.
   * @throws ClassCastException
   */
  public int compareTo(Object o) throws ClassCastException
  {
    return compareTo( (FibNumber) o);
  }

  private static final int SIZE_ENSURE = -2;
  private static final int SIZE_INCREASE = -3;
  private static final int SIZE_ADD_MARGIN = -4;

  private static final int MARGIN = 4;

  private void resizeBuffer(int size, int type)
  {
    int cl = coef.length;
    switch (type) {
      case SIZE_ENSURE:
        size = Math.max(cl, size);
        break;
      case SIZE_INCREASE:
        size += cl;
        break;
      case SIZE_ADD_MARGIN:
        size = Math.max(digits(), size) + MARGIN;
        break;
      default:
    } //switch
    if (cl >= size) {
      return;
    }

    boolean[] newCoef = new boolean[size];
    Arrays.fill(newCoef, false);
    System.arraycopy(coef, 0, newCoef, 0, Math.min(coef.length, newCoef.length));
    coef = newCoef;
  }

  private int digits()
  {
    for (int i = coef.length - 1; i > 0; i--) {
      if (coef[i]) {
        return (i + 1);
      } //if
    } //for
    return 0;
  }

  /** Converts sequences "011" to "100". Starts at position  <code>k</code> and
   * continues as long as required.
   * @param k starting position.
   * @return position where functin ended. It's greater then <code>k</code>.
   */
  private int up(int k)
  {
    while (coef[k]) {
      k++;
    } //while
    int next = k;
    boolean chain = false;
    k--; // coef[k] is last 1 in sequence
    while ( (k > 0) && coef[k] && coef[k - 1]) {
      coef[k] = false;
      coef[k - 1] = false;
      coef[k + 1] = true;
      k -= 2;
      chain = true;
    } //while
    if (chain) {
      next = up(next);
    }
    return next;
  }

  private void normalize()
  {
    resizeBuffer(0, SIZE_ADD_MARGIN);
    coef[0] = true;
    int k = 0;
    while (k < coef.length) {
      if (coef[k]) {
        k = up(k);
      } else {
        k++;
      }
    }
    coef[0] = false;
    if (digits() == 0) { // get rid of -0
      sign = PLUS;
    }
  }

  /** Add Fib(n), ie: try to set coef[n] to true
   * @param n specifies index of coefficient
   */
  private void doAdd1(int n)
  {
    if (coef[n]) {
      doAdd1(n - 1);
      doAdd1(n - 2);
    } else {
      coef[n] = true;
      up(n);
    }
  }
  /** Add number in parameter to this number
   * @param addent number to be added
   * @return returns result of this+addent
   */
  private FibNumber doAdd(FibNumber addent)
  {
    int d = addent.digits();
    resizeBuffer(d, SIZE_ADD_MARGIN);
    for (int i = 2; i < d; i++) {
      if (addent.coef[i]) {
        doAdd1(i);
      } //if
    } //for
    return this;
  }

  private void doSub1(int n)
  {
    if (coef[n]) {
      coef[n] = false;
      return;
    }
    int k = n;
    while (!coef[k]) {
      k++;
    }
    while (k > n) {
      coef[k] = false;
      if ( (k - 1) == n) {
        doAdd1(k - 2);
        break;
      } else if ( (k - 2) == n) {
        doAdd1(k - 1);
        break;
      } else {
        coef[k - 1] = true;
        coef[k - 2] = true;
      }
      k -= 2;
    }
  }

  private FibNumber doSub(FibNumber subtractor)
  {
    int d = subtractor.digits();
    for (int i = d - 1; i > 1; i--) {
      if (subtractor.coef[i]) {
        doSub1(i);
      } //if
    } //for
    return this;
  }

  public FibNumber add(FibNumber b)
  {
    return doSum(b, PLUS); // return this + b
  }

  public FibNumber subtract(FibNumber b)
  {
    return doSum(b, MINUS); // return this - b
  }

  private FibNumber doSum(FibNumber b, boolean op)
  {
    boolean AgtB = (absCompare(b) > 0);
    FibNumber result;
    if (op ^ (sign != b.sign)) { // find apropriate operation
      result = (new FibNumber(this)).doAdd(b);
    } else {
      if (AgtB) {
        result = (new FibNumber(this)).doSub(b);
      } else {
        result = (new FibNumber(b)).doSub(this);
      }
    }
    if (AgtB) { // find sign of result
      result.sign = sign;
    } else {
      result.sign = ! (op ^ b.sign);
    }
    result.normalize();
    return result;
  }

  /**
   * Converts long value into number in Fib. system
   * @param value given number
   */
  private void setValue(long value)
  {
    sign = PLUS;
    if (value < 0) {
      sign = MINUS;
      value = -value;
    }
    long[] fibList = new long[95];
    fibList[0] = 0;
    fibList[1] = 1;
    fibList[2] = 1;
    int i = 2;
    while (value > fibList[i]) {   // calculate enough Fib. numbers
      i++;
      fibList[i] = fibList[i - 1] + fibList[i - 2];
    }
    resizeBuffer(i + MARGIN, SIZE_ENSURE);
    Arrays.fill(coef, false);
    while (value > 0) {
      if (value > fibList[i]) {
        value -= fibList[i];
        coef[i] = true;
      } //if
      i--;
    }
  }

  /** Reads number from String.
   * @param value Fib. number as String
   * @return returns false when fails.
   */
  private boolean setValue(String value)
  {
    resizeBuffer(value.length() + 2 + MARGIN, SIZE_ENSURE);
    sign = PLUS;
    int end = 0;
    if (value.charAt(0) == '-') {
      sign = MINUS;
      end = 1;
    }
    if (value.charAt(0) == '+') {
      end = 1;
    }
    int out = 2;
    for (int i = value.length() - 1; i >= end; i--) {
      switch (value.charAt(i)) {
        case '1':
          coef[out] = true;
          break;
        case '0':
          break;
        default:
          return false;
      } //switch
      out++;
    } //for
    normalize();
    return true;
  }

  /**
   * Converts String value into number in Fib. system
   * @param value number as String
   * @return new FibNumber object
   * @throws NumberFormatException
   */
  public static FibNumber decode(String value) throws NumberFormatException
  {
    FibNumber result = new FibNumber();
    if ( (value == null) || (value.length() == 0) || (!result.setValue(value))) {
      throw new NumberFormatException();
    }
    return result;
  }

}
