/* Insurance Management System (Cars, Properties)

Insurance Management System (Cars, Properties)
Author: Justin Soyke (801840043)
Usage: java Assignment3 [Option] [Args]

--interactive/-i                                : Launch Interactive Mode
--list/-l [cars, properties, all]               : List Database Contents
--add/-a [cars, properties] Data                : Add Data to Database
--update/-u [cars, properties] [ID] [Data]      : Update Specific Entry
--delete/-d [cars, properties] [ID]             : Delete Specific Entry
--search/-s [cars, properties, all] [Query]     : Search Database
--import/-in [cars, properties], [Filename]     : Import Data into Database

Syntax Example:
Interactive Mode: java Assignment3 --interactive
CommandLine Mode: java Assignment3 --list cars
 */

import java.io.*;
import java.util.Scanner;

class Node<T> {
    public T data;
    public Node next;
    public Node() { this.data = null;this.next = null; }
    public Node(T data) { this.data = data;this.next = null; }
    public Node getNext() { return next; }
    public void setNext(Node<T> node) {
        // Set Next Node
        this.next = node;
    }
    public void setData(T data) {this.data = data;}
        // Set Node Data

    public T getData() { return data; }
        // Return Node Data
    }

class LinkedList<T>  {
    private int size;
    private Node<T> head;
    public LinkedList() {
        this.size = 0;
        this.head = null;
    }
    public int size() {
        return size;
    }

    public void addStart(T data) {
        // Create Initial Node
        Node<T> node = new Node<>(data);
        node.next = head;
        head = node;
        size++;
    }

    public void add(T data) {
        // Add Data to End
        if (head == null) {
            addStart(data);
        } else {
            Node<T> current = head;
            while (current.getNext() != null) {
                current = current.getNext();
            }
            Node<T> node = new Node<>(data);
            current.next = node;
            size++;
        }
    }

    public String findNode(int location) {
        // Find Node by Location
        Node node = head;
        String result = "";
        if (head != null && location <= size) {
            for (int i = 0; i < location; i++) {
                node = node.next;
            }
            result = String.valueOf(node.data);
        }
        return result;
    }

    public String findNode(String query) {
        // Find Node by Query
        String result = "";
        for (int i = 0; i < size; i++) {
            if (findNode(i).contains(query)) {
                result+="("+i+") "+ findNode(i) + "\n";
            }
        }
        return result;
    }

    public Node getNode(int location) {
        // Return Node at Location
        Node node = head;
        if (head != null && location <= size) {
            for (int i = 0; i < location - 1; i++) {
                node = node.next;
            }
            return node;
        }
        return null;
    }

    public String displayList(String format) {
        // Display LinkedList: List, CSV, Output
        Node current = head;
        String results = "";
        int count = -1;
        switch (format) {
            case "list" -> {
                // List Format
                results += "Displaying Data as: " + format + "\n";
                while (current != null) {
                    String temp = String.valueOf(current.data);
                    count = count + 1;
                    results += "(" + count + ") " + temp + "\n";
                    //   current.getData();
                    current = current.getNext();
                }
                return results;
            }
            case "csv" -> {
                // CSV Format
                results += "Displaying Data as: " + format + "\n(ID) (Data)\n";
                while (current != null) {
                    String temp = String.valueOf(current.getData());
                    results += temp + ",";
                    //   current.getData();
                    current = current.getNext();
                }
                return results;
            }
            case "output" -> {
                while (current!= null) {
                    String temp = String.valueOf(current.getData());
                    results+= temp+"\n";
                    current = current.getNext();
                }
                return results;
            }
        }
        return null;
    }

    public void remove(int location) {
        // Remove Node at Location
        Node current = head;
        Node previous = null;
        if (current != null && location <= size) {
            for (int i = 0; i < location; i++) {
                previous = current;
                current = current.next;
            }
            previous.setNext(current.next);
            size--;
        }
    }

    public void update(int location, String data) {
        // Update Data in specific location
        Node current = head;
        if (current != null && location <= size) {
            for (int i = 0; i < location; i++) {
                current = current.next;
            }
            current.setData(data);
        }
    }

    public void sort(String sortType) {
        // Not Yet Implemented
    }
}

public class Assignment3 {
    //LinkedList<String> accounts = new LinkedList<>();
    LinkedList<String> cars = new LinkedList<>();
    LinkedList<String> properties = new LinkedList<>();
    LinkedList<String> temp = new LinkedList<>();
    final static String mainHelp =
            "Insurance Management System (Cars, Properties)\nAuthor: Justin Soyke (801840043)\n" +
            "Usage: java Assignment3 [Option] [Args]\n\n" +
            "--interactive/-i\t\t\t\t: Launch Interactive Mode\n" +
            "--list/-l [cars, properties, all]\t\t: List Database Contents\n" +
            "--add/-a [cars, properties] Data\t\t: Add Data to Database\n" +
            "--update/-u [cars, properties] [ID] [Data]\t: Update Specific Entry\n" +
            "--delete/-d [cars, properties] [ID]\t\t: Delete Specific Entry\n" +
            "--search/-s [cars, properties, all] [Query]\t: Search Database\n" +
            "--import/-in [cars, properties], [Filename]\t: Import Data into Database\n" +
            "--sort [Filename] (asc/desc)\t\t: Sort Input File\n\n" +
            "Syntax Example: \nInteractive Mode: java Assignment3 --interactive\nCommandLine Mode: java Assignment3 --list cars\n";

    public static void main(String[] args) throws IOException {
        try {
            Assignment3 a = new Assignment3();
            System.out.println(mainHelp);
            a.loadData("cars", "cars.csv");
            a.loadData("properties", "properties.csv");
            switch (args[0]) {
                case "--interactive", "-i" -> a.mainMenu();
                case "--list", "-l" -> {
                    // --list cars
                    switch (args[1]) {
                        case "cars" -> System.out.println(a.cars.displayList("output"));
                        case "properties" -> System.out.println(a.properties.displayList("output"));
                        case "all" -> {
                            System.out.println(a.cars.displayList("output"));
                            System.out.println(a.properties.displayList("output"));
                        }
                    }
                }
                case "--add", "-a" -> {
                    // --add cars [Data]
                    switch (args[1]) {
                        case "cars" -> a.cars.add(args[2]);
                        case "properties" -> a.properties.add(args[2]);
                    }
                }
                case "--update", "-u" -> {
                    // --update [db] [id] [data]
                    switch (args[1]) {
                        case "cars" -> a.cars.update(Integer.parseInt(args[2]), args[3]);
                        case "properties" -> a.properties.update(Integer.parseInt(args[2]), args[3]);
                    }
                }
                case "--delete", "-d" -> {
                    // --delete [db] [id]
                    switch (args[1]) {
                        case "cars" -> a.cars.remove(Integer.parseInt(args[2]));
                        case "properties" -> a.properties.remove(Integer.parseInt(args[2]));
                    }
                }
                case "--import", "-in" -> {
                    // --import [db] [filename]
                    switch (args[1]) {
                        case "cars", "properties" -> a.loadData(args[1], args[2]);
                    }
                }
                case "--search", "-s" -> {
                    // --search cars "[Car]"
                    switch (args[1]) {
                        case "cars" -> System.out.println(a.cars.findNode(args[2]));
                        case "properties" -> System.out.println(a.properties.findNode(args[2]));
                    }
                }
                case "--sort" -> { // Not Finished
                    // --sort [Filename] [Sort]
                    // --sort data.csv asc
                    switch (args[2]) {
                        case "ascending", "asc" -> {
                            // Sort Data Ascending
                            a.sortData(args[2], "asc");
                        }
                        case "descending", "desc" -> {
                            // Sort Data Descending
                            a.sortData(args[2], "desc");

                        }
                    }
                } default -> a.mainMenu();
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ArrayIndexOutOfBoundsException e) {
            Assignment3 a = new Assignment3();
            a.loadData("cars", "cars.csv");
            a.loadData("properties", "properties.csv");
            System.out.println(mainHelp+"\n\nError: Syntax Error\nDefaulting to Interactive\n");
            a.mainMenu();

        }
    }

    public void mainMenu() {
        // Main Menu
        String menu = "\nEnter Option: \n(1) System Menu\n(2) Cars Menu\n(3) Property Menu\n(4) Exit\n";
        System.out.print(menu);
        Scanner input = new Scanner(System.in);
        int option = input.nextInt();
        switch (option) {
            case 1 -> showMenu("system");
            case 2 -> showMenu("cars");
            case 3 -> showMenu("properties");
            case 4 -> {
                System.out.println("Exiting Application");
                System.exit(0);
            } default -> {
                System.out.println("Error: No such menu");
                mainMenu();
            }
        }
    }

    public void showMenu(String type) {
        try {
            Scanner input = new Scanner(System.in);
            switch (type) {
                case "cars", "properties" -> {
                    System.out.printf("\nEnter Option: \n(1) List %s\n(2) Add %s\n(3) Delete %s\n(4) Edit %s\n(5) Search Database\n(6) Save Database\n(7) Main Menu\n(8) Exit\n",
                            type, type, type, type, type);
                    int option = input.nextInt();
                    switch (option) {
                        case 1 -> listData(type);
                        case 2 -> addMenu(type);
                        case 3 -> deleteData(type);
                        case 4 -> editData(type);
                        case 5 -> findData(type);
                        case 6 -> saveData(type);
                        case 7 -> mainMenu();
                        case 8 -> {
                            System.out.println("Exiting Application");
                            System.exit(0);
                        }
                    }
                }
                case "system" -> {
                    System.out.println("\nEnter Option: \n(1) Import Database\n(2) Main Menu\n(3) Exit\n");
                    int option = input.nextInt();
                    switch (option) {
                        case 1 -> {
                            System.out.println("Enter Database [cars|properties]: ");
                            String database = input.next();
                            System.out.println("Enter Filename: ");
                            String filename = input.next();
                            loadData(database, filename);
                        }
                        case 2 -> mainMenu();
                        case 3 -> {
                            System.out.println("Exiting Application");
                            System.exit(0);
                        }
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();

        } finally { showMenu(type); }
    }
    public void addMenu(String type) {
        System.out.printf("\nEnter Data to add to %s Database.\n", type);
        Scanner input = new Scanner(System.in);
        String inputData = input.next();
        addData(type, inputData);
        switch (type) {
            case "cars" -> System.out.println(cars.displayList("csv"));
            case "properties" -> System.out.println(properties.displayList("csv"));
        }
    }
    public  void listData(String type) {
        System.out.printf("Listing Data: %s\n", type);
        switch (type) {
            case "cars" -> System.out.println(cars.displayList("output"));
            case "properties" -> System.out.println(properties.displayList("output"));
        }
       // showMenu(type);
    }
    public  void addData(String type, String data) {
        switch (type) {
            case "cars" -> cars.add(data);
            case "properties" -> properties.add(data);
        }
       // System.out.printf("Added Data: %s to %s\n", data, type);
        //showMenu(type);
    }
    public void findData(String type) {
        System.out.println("Enter Search Query: ");
        Scanner input = new Scanner(System.in);
        String inputData = input.next();
        if (type.equals("cars")) {
            System.out.printf("Found %s:\n %s\n", inputData, cars.findNode(inputData));
        } else if (type.equals("properties")) {
            System.out.printf("Found %s:\n %s\n", inputData, properties.findNode(inputData));
        }
    }

    public void editData(String type) {
        Scanner input = new Scanner(System.in);
        switch (type) {
            case "cars" -> {
                System.out.println(cars.displayList("list"));
                System.out.println("Enter (ID) to Edit.");
                int location = input.nextInt();
                System.out.println("Enter (Data):");
                String inputData = input.next();
                cars.update(location, inputData);
            }
            case "properties" -> {
                System.out.println(properties.displayList("list"));
            }
        }
    }
    public void deleteData(String type) {
        System.out.printf("Deleting Data in %s\n", type);
        System.out.println("Enter ID to delete: ");
        Scanner input = new Scanner(System.in);
        //String choice = input.next();
        switch (type) {
            case "cars" -> {
                int id = input.nextInt();
                cars.remove(id);
            }
            case "properties" -> {
                int id = input.nextInt();
                properties.remove(id);
            }
        }
    }
    public void saveData(String type) {
        switch (type) {
            case "cars" -> {
                System.out.printf("Saving %s Database\n", type);
                String results = cars.displayList("output");
                //System.out.println("Results: "+ results);
                writeData(type, results);
            }
            case "properties" -> {
                System.out.printf("Saving %s Database\n", type);
                String results = properties.displayList("output");
                writeData(type, results);
            }
        }
    }
    public void writeData(String type, String data) {
        switch (type) {
            case "cars", "properties" -> {
                try {

                    FileWriter out = new FileWriter(type+".csv");
                    BufferedWriter bOut = new BufferedWriter(out);
                    System.out.printf("Type: %s\nData: \n%s\n", type, data);
                    bOut.write(data);
                    bOut.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
    public void loadData(String type, String file) throws IOException {
        FileReader in = new FileReader(file);
        BufferedReader bIn = new BufferedReader(in);
        String line;
        switch (type) {
            case "cars" -> {
                while ((line = bIn.readLine()) != null) {
                    cars.add(line);
                    //System.out.printf("Reading Data from %s: %s\n", type, line);
                } saveData(type);
            }
            case "properties" -> {
                while ((line = bIn.readLine()) != null) {
                    properties.add(line);
                    //System.out.printf("Reading Data from %s: %s\n", type, line);
                } saveData(type);
            }
            case "temp" -> {
                while ((line = bIn.readLine()) != null) {
                    temp.add(line);
                }
            }
        }
    }
    public void sortData(String sortType, String filename) throws IOException {
        // Not Finished
        System.out.println("Error: Feature not yet implemented");
        //loadData("temp", filename);
        //temp.sort("asc");


    }
}

