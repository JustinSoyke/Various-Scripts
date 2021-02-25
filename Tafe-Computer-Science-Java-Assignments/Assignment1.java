/*
Coding Assignment 1 - 3/08/2020
Justin Soyke 
Problem: Write a program that given a 4 digit number from keyboard, applies Kaprekar's operation and discover how many
steps it takes to get to the Kernel number 6174.
 */

// Imports
import java.util.*;

public class Assignment1 {
    // Assignment1 Class

    public static void main(String[] args) {
        //
        String banner = "+==================================+" +
                        "\n+ Kaprekar's Operation Application +" +
                        "\n+ Author: Justin Soyke  +" +
                        "\n+==================================+";
        System.out.println(banner);
        mainMenu();
        };

    public static void mainMenu() {
        // Main Program Menu
        System.out.print("\nEnter Option:\n\n(1) Continue\n(2) Exit\n");
        try {
            Scanner input = new Scanner(System.in);
            int option = input.nextInt();
            switch (option) {
                case 1 -> kaprekarMenu();
                case 2 -> {
                    System.out.println("Exiting Application");
                    System.exit(0);
                }
                default -> {
                    System.out.println("Error: Invalid Option");
                    mainMenu();
                }
            }
        } catch (InputMismatchException e) {
            System.out.println("Error Invalid Input");
            mainMenu();
        } catch (NumberFormatException e) {
            System.out.println("Error: Not a number");
            kaprekarMenu();
        }
    }

    public static void kaprekarMenu() {
        // Show Menu
        try {
            System.out.println("Enter valid 4-digit number: \n");
            Scanner input = new Scanner(System.in);
            String math = input.next();
            kaprekar(math);
            mainMenu();
        } catch (NumberFormatException e) {
            System.out.println("Error: Not a number");
            kaprekarMenu();
        } finally {
            mainMenu();
        }
    }

    public static void kaprekar(String num) {
        // do kaprekar operation
        int counter = 0;
        ArrayList<String> kapLog = new ArrayList<>();
        String currentNum = num;
        while (true) {
            if (currentNum.equals("6174")) {
                kapLog.add(currentNum);
                System.out.printf("Kernel Number Reached in %d steps.\n", counter);
                System.out.printf("Kaprekar Log: %s", kapLog);
                break;
            } else if (counter==10000){
                System.out.printf("Unable to find Kernel Number in %d steps.\nPlease try again.\n", counter);
                kaprekarMenu();
                break;
            } else {
                kapLog.add(currentNum); // Add Number to Kaprekar Log
                currentNum = doMath(currentNum);
                counter++; // Increase Counter
            }
        }
    }

    public static String doMath(String num) {
        // Do Math
        List<String> minMax = Arrays.asList(num.split(""));       // Create Array as List
        Collections.sort(minMax);                                       // Sort List Low > High
        String minStr = String.join("", minMax);               // Create String from Array
        Integer minInt = Integer.parseInt(minStr);                     // Convert String to Integer
        Collections.sort(minMax, Comparator.reverseOrder());           // Sort in Reverse Order
        String maxStr = String.join("", minMax);
        Integer maxInt = Integer.parseInt(maxStr);
        Integer kapResult = maxInt-minInt;
        return kapResult.toString();    // Return Result as String
    }

}
