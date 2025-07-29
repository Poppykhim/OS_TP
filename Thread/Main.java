package Thread;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Main {

    public static void main(String[] args) {
        // new Thread(new SimpleTask()).start();
        ExecutorService executor = Executors.newSingleThreadExecutor();
        executor.execute(new SimpleTask());
        executor.shutdown();
    }
}
