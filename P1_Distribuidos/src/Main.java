import java.util.Arrays;
import java.util.List;

// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public class Main {
    public static void main(String[] args) {
        List<Double>lista1= Arrays.asList(1.5, 2.0, 3.9, 1.2);
        List<Double>lista2=Arrays.asList(2.2, 6.3, 8.8, 3.3, 0.5);
        Thread union=new Thread(new Hilo("Unir", lista1, lista2));
        Thread sort=new Thread(new Hilo("Ordenar", lista1, lista2));
        Thread comp=new Thread(new Hilo("Comp", lista1, lista2));
        Thread maxmin=new Thread(new Hilo("MaxMin", lista1, lista2));

        union.start();
        sort.start();
        comp.start();
        maxmin.start();
    }
}