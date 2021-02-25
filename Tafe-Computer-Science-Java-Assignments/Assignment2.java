/*
Coding Assignment 2 - 17/08/2020
Author: Justin Soyke 

1. Write a Java application which given an IP address in decimal dotted notation and
subnet mask in CIDR ( prefix format):
    - Class
    - Host, Network, Broadcast?
    - If host or broadcast, determine network address
    - For each network address display Total Hosts, First/Last Usable, Broadcast

Class           Range                   Subnet Mask         CIDR    Binary
A       0.0.0.0     - 127.255.255.255    255.0.0.0          /8      11111111.00000000.00000000.00000000
B       128.0.0.0   - 191.255.255.255    255.255.0.0        /16     11111111.11111111.00000000.00000000
C       192.0.0.0   - 223.255.255.255    255.255.255.0      /24     11111111.11111111.11111111.00000000
D       224.0.0.0   - 239.255.255.255    255.255.255.255    /32     11111111.11111111.11111111.11111111

Class   Subnet Mask         Decimal
A       255.0.0.0           4278190080
B       255.255.0.0         4294901760
C       255.255.255.0       4294967040
D       255.255.255.255     4294967295


*/
import java.util.*;
import java.lang.Math;


class myMath {
    public static long calcPower(int x, int y) {
        // Calculate Powers:  x^y
        return (long) Math.pow(x, y);
    }

    public static long binToInt(String bin) {
        /* Convert Binary to Integer
        Input:  Binary   11111111
        Output: Decimal  255
         */
        return Long.parseLong(bin, 2);
    }

    public static String decToBin(String ip) {
        /* Convert decimal to Binary
        Input: 3232235521
        Output: 11000000101010000000000000000001
         */
        String b = Long.toBinaryString(Long.parseLong(ip));
        String add = "";
        if (b.length() < 32) {
            add = "0".repeat(32 - b.length());
        }
        return add + b;
    }

    public static String fromIp(String ip, String type) {
        /* Convert IP to Decimal or Binary
        first*(256)^3 + second*(256)^2 + third*(256)^1 + forth*(256)^0 = Base256 IP
        Input:  IP 192.168.0.1, Type: Binary, Output: 11000000101010000000000000000001
        Output: IP 192.168.0.1, Type: Decimal, Output: 3232235521
        */
        ArrayList<Integer> octList = new ArrayList<>(); // create new integer array
        String[] ipSplit = ip.split("\\.", 4);
        ArrayList<Long> octTest = new ArrayList<>();    // create long arraylist
        String result = "";
        long dec = 0;   // Initialize long for decimal IP
        int pow = 3;    // Initialize starting power
        for (String oct : ipSplit) {    // for octet in ip
            int tempNum = Integer.parseInt(oct);
            octList.add(tempNum);
        }
        while (pow > -1) {  // While Power greater than -1
            for (Integer o : octList) {
                octTest.add(o * calcPower(256, pow));   // add octlet*(256)^pow to decimal array
                --pow; // Reduce Power by 1
            }
        }
        for (Long l : octTest) {
            dec += l;
        }
        if (type.equals("binary")) {
            result = decToBin(String.valueOf(dec));
        } else if (type.equals("decimal")) {
            result = String.valueOf(dec);
        }
        return result;
    }

   public static String toIp(String data, String type) {
        /* Create IP Address Representation of Input Data
        Input Data: 11000000101010000000000000000001, Type: Binary, Output: 192.168.0.1
        Input Data: 3232235521, Type: Decimal, Output: 192.168.0.1
        Input Data: 3232235520, Type: First, Output: 192.168.0.1    (Network Address + 1)
        Input Data: 3232235775, Type: Last, Output: 192.168.0.254   (Broadcast Address -1)
         */
        String result = "";
        String test;
        long temp;
       switch (type) {
           case "binary" -> result = binToIp(decToBin(data));
           case "decimal" -> {
               test = decToBin(data);
               result = binToIp(test);
           }
           case "first" -> {
               temp = Long.parseLong(data, 2);
               test = decToBin(String.valueOf(temp + 1));
               result = binToIp(test);
           }
           case "last" -> {
               temp = Long.parseLong(data, 2);
               test = decToBin(String.valueOf(temp - 1));
               result = binToIp(test);
           }
       }
        return result;
   }

    public static String binToIp(String n) {
        /* Convert Binary to IP Address
        Input: Binary 11000000101010000000000000000001
        Output: IP 192.168.0.1
         */
        ArrayList<String> ipSplit = new ArrayList<>();
        int start = 0;
        int end = 8;
        String temp;
        String ip;
        for (int i = 0; i<4; i++) {
            temp = n.substring(start, end);
            ipSplit.add(String.valueOf(binToInt(temp)));
            start+=8; // increment by octet
            end+=8;
        }
        ip = String.join(".", ipSplit); // Create IP from Array
        return ip;
    }

    public static String getNet(String ipBin, int cidr) throws InputMismatchException {
        /* Get Network Address from IP, CIDR Input
        Input: Binary 11000000101010000000000000000001
        Input: Integer 24
        Output: 11000000101010000000000000000000
         */
        String ip = fromIp(ipBin, "binary");
        String net = ip.substring(0, cidr);
        String hostBit = "0".repeat(32-cidr);
        return binToIp(net+hostBit);
    }

    public static String getBroadcast(String ip, int cidr) {
        /* Get Broadcast Address from IP, CIDR Input
        Input: Binary 11000000101010000000000000000001
        Input: Integer 24
        Output: 11000000101010000000000011111111
         */
        String net = ip.substring(0, cidr);
        return binToIp(net+"1".repeat(32-cidr)); // Broadcast
    }

    public static String getMask(int cidr) {
        /* Get Binary Subnet Mask from Integer CIDR
        Input: Integer 24
        Output: 11111111111111111111111100000000
         */
        final int ipLen = 32;
        String net = "1".repeat(cidr);
        String host = "0".repeat(ipLen-cidr);
        return binToIp(net+host);
    }

    public static String getClass(String ip) {
        /* Get Network Class from Binary IP
        Input: Binary 11000000101010000000000000000001
        Output: C
         */
        String result;
        boolean A = ip.subSequence(0, 1).equals("0");       // Class A (0xxx)
        boolean B = ip.subSequence(0, 2).equals("10");      // Class B (10xx)
        boolean C = ip.subSequence(0, 3).equals("110");     // Class C (110x)
        boolean D = ip.subSequence(0, 4).equals("1110");    // Class D (1110)
        boolean E = ip.subSequence(0, 4).equals("1111");    // Class E (1111)
        result = (A ? "A" : B ? "B" : C ? "C" : D ? "D" : E ? "E" : null);
        return result;
    }
}

public class Assignment2 {
    public static void main(String[] args) {
        final String banner = "+==================================+" +
                "\n+ IP Tools +" +
                "\n+ Author: Justin Soyke +" +
                "\n+==================================+";
        System.out.println(banner);
        mainMenu();
    }

    public static void mainMenu() {
        /* Main Program Menu
        Input: 1 -> IP Analysis
        Input: 2 -> Exit Application
         */
        String banner = "\nEnter Option: \n(1) IP Analysis\n(2) Exit\n";
        System.out.print(banner);
        try {
            Scanner input = new Scanner(System.in);
            int option = input.nextInt();
            switch (option) {
                case 1 -> ipMenu();
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
            System.out.println("Error: Invalid Input");
            mainMenu();
        } catch (NumberFormatException e) {
            System.out.println("Error: Invalid Option");
        }
    }
    public static void ipMenu() {
        /* IP Analysis
        Input: 192.168.0.1/24
        Output: IP: 192.168.0.1 -- CIDR: 24 -- Subnet Mask: 255.255.255.0 -- Type: Host -- Class: C
                Network Address: 192.168.0.0 -- Broadcast Address: 192.168.0.255
                Total Usable Hosts: 254 -- First: 192.168.0.1 -- Last: 192.168.0.254
         */
        try {
            System.out.println("Enter IP+Mask (127.0.0.1/24): ");
            Scanner input = new Scanner(System.in);
            String ipIn = input.next();
            String[] ipSplit = ipIn.split("/", 2);
            String ip = ipSplit[0];
            int cidr = Integer.parseInt(ipSplit[1]);
            String decIp = myMath.fromIp(ip, "decimal"); // Decimal IP
            String binIp = myMath.fromIp(ip, "binary"); // Binary IP
            String netIp = myMath.getNet(ip, cidr); // Network Address
            String netClass = myMath.getClass(binIp); // Network Class
            String broadcast = myMath.getBroadcast(myMath.fromIp(ip, "binary"), cidr); // Broadcast Address
            String netmask = myMath.getMask(cidr); // Subnet Mask
            String type; // Type of Address
            if (netIp.equals(ip)) {
                type = "Network";
            } else if (ip.equals(broadcast)) {
                type = "Broadcast";
            } else {
                type = "Host";
            }
            System.out.printf("IP: %s -- CIDR: %s -- Subnet Mask: %s -- Type: %s -- Class: %s\nNetwork Address: %s -- Broadcast Address: %s\n",
                    ip, cidr, netmask, type, netClass, netIp, broadcast);
            System.out.printf("Total Usable Hosts: %s -- First: %s -- Last: %s\n", myMath.calcPower(2, 32 - cidr) - 2,
                    myMath.toIp(myMath.fromIp(netIp, "binary"), "first"),
                    myMath.toIp(myMath.fromIp(broadcast, "binary"), "last"));

            mainMenu();
        } catch (InputMismatchException e) {
            System.out.println("Error: Invalid Input");
            ipMenu();
        } catch (NumberFormatException e) {
            System.out.println("Error: Invalid IP");
            ipMenu();
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Error: Invalid IP+CIDR");
            ipMenu();
        } catch (StringIndexOutOfBoundsException e) {
            System.out.println("Error: Invalid CIDR");
            ipMenu();
        } catch (Exception e) {
            System.out.printf("\nError: %s\n", e);
        } finally {
            mainMenu();
        }
    }
}
