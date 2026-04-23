import java.util.*;

class InSufficientFundsException extends Exception {
    public InSufficientFundsException(String message) {
        super(message);
    }
}

class Account {
    private String accountHolder;
    private double balance;
    private ArrayList<Double> transactions;

    public Account(String accountHolder, double balance) {
        this.accountHolder = accountHolder;
        this.balance = balance;
        this.transactions = new ArrayList<>();
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }

        balance += amount;
        addTransaction(amount);
        System.out.println("Deposited: " + amount);
    }

    public void processTransaction(double amount) throws InSufficientFundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }

        if (amount > balance) {
            throw new InSufficientFundsException("Insufficient balance. Current balance: " + balance);
        }

        balance -= amount;
        addTransaction(-amount);
        System.out.println("Spent: " + amount);
    }

    private void addTransaction(double amount) {
        if (transactions.size() >= 5) {
            transactions.remove(0);
        }
        transactions.add(amount);
    }

    public void printMiniStatement() {
        System.out.println("\n--- MINI STATEMENT ---");
        System.out.println("Account: " + accountHolder);
        System.out.println("Balance: " + balance);

        if (transactions.isEmpty()) {
            System.out.println("No transactions yet");
            return;
        }

        for (double t : transactions) {
            if (t > 0)
                System.out.println("Deposit: " + t);
            else
                System.out.println("Withdraw: " + Math.abs(t));
        }
    }

    public double getBalance() {
        return balance;
    }
}

public class FinSafeApp {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Welcome to FinSafe");

        System.out.print("Enter Account Holder Name: ");
        String name = sc.nextLine();

        System.out.print("Enter Initial Balance: ");
        double bal = Double.parseDouble(sc.nextLine());

        Account acc = new Account(name, bal);

        while (true) {
            System.out.println("\n1. Deposit");
            System.out.println("2. Spend");
            System.out.println("3. Mini Statement");
            System.out.println("4. Check Balance");
            System.out.println("5. Exit");
            System.out.print("Enter choice: ");

            String choice = sc.nextLine();

            try {
                switch (choice) {
                    case "1":
                        System.out.print("Enter deposit amount: ");
                        double d = Double.parseDouble(sc.nextLine());
                        acc.deposit(d);
                        break;

                    case "2":
                        System.out.print("Enter spend amount: ");
                        double w = Double.parseDouble(sc.nextLine());
                        acc.processTransaction(w);
                        break;

                    case "3":
                        acc.printMiniStatement();
                        break;

                    case "4":
                        System.out.println("Balance: " + acc.getBalance());
                        break;

                    case "5":
                        System.out.println("Thank you for using FinSafe");
                        return;

                    default:
                        System.out.println("Invalid choice");
                }

            } catch (NumberFormatException e) {
                System.out.println("Enter valid number");
            } catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            } catch (InSufficientFundsException e) {
                System.out.println(e.getMessage());
            }
        }
    }
}