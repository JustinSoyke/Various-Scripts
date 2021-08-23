/*
Fundamentals of Computer Science Final Coding Assignment
Author: Justin Soyke (801840043)

Write a Java application which builds a binary expressing tree using inflix expression format.
Make sure you take into account precedence rule (brackets > * > * / > + -) and associativity rule
(R to L for ^ and L to R for other operators). Application should have a display option to show in-order, pre-order and
post-order of the given expression. Your application should also be able to be run from command line where if the
expression to be evaluated is given as part of the argument, it is evaluated and result is displayed. If application is
run without any operand then a text based menu is displayed with all the options specified. In your design of data structures
make sure you consider:
1. Java abstract and/or Interface classes where appropriate
2. Function overloading and overriding
3. Operator overloading.
4. Appropriate use public, private access control on instance variable, methods
5. Your classes should implement getter and setters

+: left + right
-: left - right
/: left / right
*: left * right

Precedence rule: brackets > ^ > * / > +-
Associativity Rule: (R to L for ^, L to R for other Operators)

Infix Example: (((2 *(10 / 5)) -3)+((3 * 10) + 7))

 */


class TreeNode {
    private String data;
    private TreeNode left;
    private TreeNode right;
    public TreeNode(String data) { this.data = data; this.left = null; this.right = null;}
    public TreeNode(String data, TreeNode left, TreeNode right) {this.data = data; this.left = left; this.right = right;}
    public TreeNode getLeft() { return left; }
    public void setLeft(TreeNode left) { this.left = left; }
    public TreeNode getRight() { return right; }
    public void setRight(TreeNode right) { this.right = right; }
    public String getData() { return data; }
    public void setData(String data) { this.data = data; }
}

class ExpressionTree {
    private TreeNode root;
    public ExpressionTree() { root = null;}

    public void addRoot(String data) {
        if (root == null) {
            this.root = new TreeNode(data);
        }
    }
    public void add(String type, String data) {
        if (root != null) {
            TreeNode node = root;
            switch (type) {
                case "left" -> node.setLeft(new TreeNode(data, null, null));
                case "right" -> node.setRight(new TreeNode(data, null, null));
                case "data" -> node.setData(data);
            }
        }
    }
    public void add(String data, TreeNode left, TreeNode right) {
        if (root == null) {
            this.root = new TreeNode(data);
        } else {
            TreeNode node = root;
            node.setData(data);
            node.setLeft(left);
            node.setRight(right);
        }
    }
    public void display(String type) {
        if (root != null) {
            switch (type) {
                case "in" -> displayInTree(root);
                case "pre" -> displayPreTree(root);
                case "post" -> displayPostTree(root);
            }
        }
    }

    public void displayInTree(TreeNode root) {
        System.out.print("(");
        if (root.getLeft() != null) {
            displayInTree(root.getLeft());
        }
        System.out.print(" " + root.getData() + " ");
        if (root.getRight() != null) {
            displayInTree(root.getRight());
        }
        System.out.print(")");
    }
    public void displayPreTree(TreeNode root) {
        System.out.print(" " + root.getData() + " ");
        if (root.getLeft() != null) {
            displayPreTree(root.getLeft());
        }
        if (root.getRight() != null) {
            displayPreTree(root.getRight());
        }
    }
    public void displayPostTree(TreeNode root) {
        if (root.getLeft() != null) {
            displayPostTree(root.getLeft());
        }
        if (root.getRight() != null) {
            displayPostTree(root.getRight());
        }
        System.out.print(" " + root.getData() + " ");
    }

}

public class FinalAssignment {
    public static void main(String[] args) {
        ExpressionTree et = new ExpressionTree();
        et.add("+", null, null);
        et.add("left", "1");
        et.add("right", "2");

        System.out.print("In-Order: ");
        et.display("in");
        System.out.print("\nPre-Order: ");
        et.display("pre");
        System.out.print("\nPost-Order: ");
        et.display("post");
    }
}
