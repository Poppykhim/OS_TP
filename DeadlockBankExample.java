
class Account {

    private int balance;
    private final int id; // to help identify accounts

    public Account(int id, int balance) {
        this.id = id;
        this.balance = balance;
    }

    public int getId() {
        return id;
    }

    public synchronized void deposit(int amount) {
        balance += amount;
    }

    public synchronized void withdraw(int amount) {
        balance -= amount;
    }

    public int getBalance() {
        return balance;
    }
}

// class Bank {
//     public static void transfer(Account from, Account to, int amount) {
//         // Lock accounts in the order they are passed
//         synchronized (from) {
//             System.out.println(Thread.currentThread().getName()
//                     + " locked Account " + from.getId());
//             // Simulate delay to make deadlock more likely
//             try {
//                 Thread.sleep(100);
//             } catch (InterruptedException e) {
//             }
//             synchronized (to) {
//                 System.out.println(Thread.currentThread().getName()
//                         + " locked Account " + to.getId());
//                 from.withdraw(amount);
//                 to.deposit(amount);
//                 System.out.println("Transfer of " + amount
//                         + " from Account " + from.getId()
//                         + " to Account " + to.getId() + " successful");
//             }
//         }
//     }
// }
class Bank {

    public static void transfer(Account from, Account to, int amount) {
        Account first;
        Account second;

        // Use min/max of account IDs (not balances, since balance changes)
        if (from.getId() == Math.min(from.getId(), to.getId())) {
            first = from;
            second = to;
        } else {
            first = to;
            second = from;
        }

        synchronized (first) {
            System.out.println(Thread.currentThread().getName()
                    + " locked Account " + first.getId());

            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
            }

            synchronized (second) {
                System.out.println(Thread.currentThread().getName()
                        + " locked Account " + second.getId());

                // Perform transfer
                from.withdraw(amount);
                to.deposit(amount);

                System.out.println("Transfer of " + amount
                        + " from Account " + from.getId()
                        + " to Account " + to.getId() + " successful");
            }
        }
    }
}

public class DeadlockBankExample {

    public static void main(String[] args) {
        Account acc1 = new Account(1, 1000);
        Account acc2 = new Account(2, 1000);

        // Thread 1 transfers from acc1 → acc2
        Thread t1 = new Thread(() -> {
            Bank.transfer(acc1, acc2, 100);
        }, "T1");

        // Thread 2 transfers from acc2 → acc1 (reverse order)
        Thread t2 = new Thread(() -> {
            Bank.transfer(acc2, acc1, 200);
        }, "T2");

        t1.start();
        t2.start();
    }
}
