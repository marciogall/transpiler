import java.util.Scanner;
import java.util.Arrays;
public class Output{

@SafeVarargs
public static <T> T[] concatAll(T[] first, T[]... rest) {
int totalLength = first.length;
for (T[] array : rest) {
totalLength += array.length;
}
T[] result = Arrays.copyOf(first, totalLength);
int offset = first.length;
for (T[] array : rest) {
System.arraycopy(array, 0, result, offset, array.length);
offset += array.length;
}
return result;
}
public static void main(String[] args){
Scanner input = new Scanner(System.in);
System.out.println("Insert your name: ");
String a = input.nextLine();
System.out.println("Insert your surname: ");
String b = input.nextLine();
System.out.println("Insert your job: ");
String c = input.nextLine();
System.out.println("Insert your age: ");
String d = input.nextLine();
String[] e = {a, b, c, };
String[] f = {d, "s", };
String[] z = concatAll(e , f);
Object len_1 = e.length;
Object len_2 = f.length;
Object len_3 = z.length;
System.out.println("The concatenation of the two lists returns:");
System.out.println(Arrays.toString(z));
System.out.println("The length of the first list is: ");
System.out.println(len_1);
System.out.println("The length of the second list is: ");
System.out.println(len_2);
System.out.println("The length of the final list is: ");
System.out.println(len_3);
}
}