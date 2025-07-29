package Thread.Thread2;

import java.util.concurrent.Callable;

public class Summations implements Callable<Integer> {

    private int upper;

    public Summations(int upper) {
        this.upper = upper;
    }

    @Override
    public Integer call() {
        int sum = 0;
        for (int i = 1; i <= upper; i++) {
            sum += i;
        }
        return sum;
    }
}
