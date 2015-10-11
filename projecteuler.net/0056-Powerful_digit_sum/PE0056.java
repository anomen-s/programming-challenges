
import java.math.BigInteger;

public class PE0056 {

    public static final int RANGE = 100;

    public static void main(String[] args)
    {
	(new PE0056()).solve();
    }
    
    public void solve() {
        start();
        BigInteger maxN = BigInteger.ZERO;
        int maxDs = 0;
        for (int a = 2; a < RANGE; a++) {
            System.out.println(a);
            BigInteger bia = BigInteger.valueOf(a);
            BigInteger n = BigInteger.ONE;
            for (int b = 1; b < RANGE; b++) {
                n = n.multiply(bia);
                int ds = digitSum(n);
                if (ds > maxDs) {
                    maxDs = ds;
                    maxN = n;
                }
            }

        }
        printTime();
        System.out.println("result " + maxN + " " + maxDs);
    }

    private int digitSum(BigInteger n) {
        int res = 0;
        while (n.compareTo(BigInteger.ZERO) > 0) {
            final BigInteger[] r = n.divideAndRemainder(BigInteger.TEN);
            res += r[1].intValue();
            n = r[0];
        }
        return res;
    }

    private long startTime = 0;

    private void start() {
        startTime = System.currentTimeMillis();
    }
    private void printTime()
    {
        long endTime = System.currentTimeMillis();
        System.out.println("time: " + (endTime-startTime) + "ms");
    }
}
