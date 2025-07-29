package Thread.Thread2;

import java.util.concurrent.*;

public class Driver {

    public static void main(String[] args) {
        int upper = Integer.parseInt(args[0].trim());

        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<Integer> result = pool.submit(new Summations(upper));

        try {
            System.out.println("sum = " + result.get());
        } catch (InterruptedException | ExecutionException ie) {
            ie.printStackTrace();
        }

        pool.shutdown();
    }
}
