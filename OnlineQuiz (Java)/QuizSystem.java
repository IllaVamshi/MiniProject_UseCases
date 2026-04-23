import java.io.*;
import java.util.*;

// -------- QUESTION CLASS --------
class Question {
    String question;
    String[] options;
    int answer;

    Question(String question, String[] options, int answer) {
        this.question = question;
        this.options = options;
        this.answer = answer;
    }

    void display() {
        System.out.println("\n" + question);
        for (int i = 0; i < 4; i++) {
            System.out.println((i + 1) + ". " + options[i]);
        }
    }

    String toFileString() {
        return question + "|" + options[0] + "|" + options[1] + "|" +
               options[2] + "|" + options[3] + "|" + answer;
    }
}

// -------- MAIN SYSTEM --------
public class QuizSystem {

    static Scanner sc = new Scanner(System.in);
    static String qFile = "questions.txt";
    static String aFile = "admin.txt";

    // -------- ADMIN PASSWORD --------
    static String getPassword() {
        try (BufferedReader br = new BufferedReader(new FileReader(aFile))) {
            return br.readLine();
        } catch (Exception e) {
            // create default password
            try (FileWriter fw = new FileWriter(aFile)) {
                fw.write("admin");
            } catch (Exception ex) {}
            return "admin";
        }
    }

    static boolean login() {
        System.out.print("Enter Admin Password: ");
        String pass = sc.nextLine();
        return pass.equals(getPassword());
    }

    // -------- FILE HANDLING --------
    static void saveQuestion(Question q) {
        try (FileWriter fw = new FileWriter(qFile, true)) {
            fw.write(q.toFileString() + "\n");
        } catch (IOException e) {
            System.out.println("Error saving question!");
        }
    }

    static List<Question> loadQuestions() {
        List<Question> list = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(qFile))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] p = line.split("\\|");
                if (p.length == 6) {
                    String q = p[0];
                    String[] opt = {p[1], p[2], p[3], p[4]};
                    int ans = Integer.parseInt(p[5]);
                    list.add(new Question(q, opt, ans));
                }
            }
        } catch (IOException e) {
            System.out.println("No questions found!");
        }

        return list;
    }

    // -------- ADMIN SECTION --------
    static void addQuestions() {
        System.out.print("Enter number of questions: ");
        int n = sc.nextInt();
        sc.nextLine();

        for (int i = 0; i < n; i++) {
            System.out.print("\nEnter question: ");
            String q = sc.nextLine();

            String[] opt = new String[4];
            for (int j = 0; j < 4; j++) {
                System.out.print("Option " + (j + 1) + ": ");
                opt[j] = sc.nextLine();
            }

            System.out.print("Correct answer (1-4): ");
            int ans = sc.nextInt();
            sc.nextLine();

            saveQuestion(new Question(q, opt, ans));
        }

        System.out.println("Questions saved successfully!");
    }

    // -------- QUIZ SECTION --------
    static void startQuiz() {
        List<Question> list = loadQuestions();

        if (list.isEmpty()) {
            System.out.println("No questions available!");
            return;
        }

        Collections.shuffle(list);

        int score = 0;
        long startTime = System.currentTimeMillis();
        long timeLimit = 60000; // 60 seconds

        for (Question q : list) {

            if (System.currentTimeMillis() - startTime > timeLimit) {
                System.out.println("\n⏰ Time's up!");
                break;
            }

            q.display();
            System.out.print("Your answer: ");

            int ans;
            try {
                ans = sc.nextInt();
            } catch (Exception e) {
                sc.next();
                System.out.println("Invalid input!");
                continue;
            }

            if (ans == q.answer) {
                score++;
            }
        }

        showResult(score, list.size());
    }

    // -------- RESULT --------
    static void showResult(int score, int total) {
        System.out.println("\n===== RESULT =====");
        System.out.println("Score: " + score + "/" + total);

        double percent = (score * 100.0) / total;
        System.out.println("Percentage: " + percent + "%");

        if (percent >= 80)
            System.out.println("Performance: Excellent");
        else if (percent >= 50)
            System.out.println("Performance: Good");
        else
            System.out.println("Performance: Needs Improvement");
    }

    // -------- MAIN MENU --------
    public static void main(String[] args) {

        while (true) {
            System.out.println("\n===== ONLINE QUIZ SYSTEM =====");
            System.out.println("1. Admin - Add Questions");
            System.out.println("2. User - Take Quiz");
            System.out.println("3. Exit");
            System.out.print("Enter choice: ");

            int choice = sc.nextInt();
            sc.nextLine();

            switch (choice) {
                case 1:
                    if (login()) {
                        addQuestions();
                    } else {
                        System.out.println("Wrong password!");
                    }
                    break;

                case 2:
                    startQuiz();
                    break;

                case 3:
                    System.out.println("Exiting...");
                    return;

                default:
                    System.out.println("Invalid choice!");
            }
        }
    }
}