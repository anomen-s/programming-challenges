import java.util.Set;
import java.util.TreeSet;

public class PE0047 {

    public static Set<Integer>[] sieve(int range) {

        Set<Integer>[] nums = new Set[range];
        for (int i = 0; i < nums.length; i++) {
            nums[i] = new TreeSet<Integer>();
        }
        for (int p = 2; 2 * p <= range; p++) {
            if (nums[p].isEmpty()) {
                int i = p + p;
                while (i < range) {
                    nums[i].add(p);
                    i = i + p;
                }
            }
        }
        return nums;
    }

    public static int RANGE = (int) 1e6;

    public static void main(String[] args) {

        Set<Integer>[] factors = sieve(RANGE);
        System.out.println("Sieve completed.");
        int SEQ = 2;
        for (int i = SEQ; i < RANGE; i++) {
            boolean found = true;
            for (int i2 = 0; i2 < SEQ; i2++) {
                if (factors[i - i2].size() != SEQ) {
                    found = false;
                }
            }
            if (found) {
                System.out.println((i-SEQ+1) + " ");
                SEQ++;
            }
        }
 
    }

}