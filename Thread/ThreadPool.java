package Thread;

import java.util.concurrent.*;

public class ThreadPool {

    public static void main(String[] args) {
        int numTasks = Integer.parseInt(args[0].trim());
        ExecutorService pool = Executors.newCachedThreadPool();
        for (int i = 0; i < numTasks; i++) {
            pool.execute(new SimpleTask());
        }

        pool.shutdown();
    }
}
