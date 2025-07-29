
public class Bank implements Runnable {

    private static int balance = 0;
    // private static final Object lock = new Object(); // Optional lock

    public void deposit() {
        // Simulate delay if needed
        // try { Thread.sleep(1000); } catch (InterruptedException e) { e.printStackTrace(); }
        balance += 100;
    }

    public void withdraw() {
        balance -= 100;
    }

    public int getValue() {
        return balance;
    }

    @Override
    public void run() {
        deposit();
        System.out.println("Value for Thread after deposit " + Thread.currentThread().getName() + ": " + getValue());
        withdraw();
        System.out.println("Value for Thread after withdraw " + Thread.currentThread().getName() + ": " + getValue());

    }

    public static void main(String[] args) {
        Bank bank = new Bank();
        Thread t1 = new Thread(bank, "Thread-1");
        Thread t2 = new Thread(bank, "Thread-2");

        t1.start();
        t2.start();
    }
}
