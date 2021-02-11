import java.util.Scanner;
import java.util.Arrays;
public class Output{
public static Object area(Object a, Object b){
Scanner input = new Scanner(System.in);
Double d = Double.parseDouble(a.toString()) * Double.parseDouble(b.toString());
return d;
}
public static void main(String[] args){
Scanner input = new Scanner(System.in);
int a = 2;
double b = 3.4;
System.out.println("The first side is ");
System.out.println(a);
System.out.println("The second side is ");
System.out.println(b);
Double c = (Double) area(a, b);
System.out.println("The area is ");
System.out.println(c);
}
}