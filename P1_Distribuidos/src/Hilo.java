import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

public class Hilo implements Runnable{
    private String op;
    private List<Double> l1, l2;
    public Hilo(String op, List<Double>l1, List<Double>l2){
        this.op=op;
        this.l1=l1;
        this.l2=l2;

    }
    @Override
    public void run(){
        List<Double> listaComb=new ArrayList<>();
        switch (op){
            case "Ordenar":
                Collections.sort(l1);
                Collections.sort(l2);
                System.out.println("Lista 1 ordenada: "+l1);
                System.out.println("Lista 2 ordenada: "+l2);
                break;
            case "Unir":
                listaComb.addAll(l1);
                listaComb.addAll(l2);
                System.out.println("Lista combinada: "+listaComb);
                break;
            case "Comp":
                if(l1.size()>l2.size())
                    System.out.println("Lista 1 mayor que lista 2");
                else if (l2.size()>l1.size()) {
                    System.out.println("Lista 2 mayor que lista 1");
                }
                else{
                    System.out.println("Ambas listas son iguales");
                }
                break;
            case "MaxMin":
                System.out.println("Lista 1 -> Máximo: " + Collections.max(l1) + ", Mínimo: " + Collections.min(l1));
                System.out.println("Lista 2 -> Máximo: " + Collections.max(l2) + ", Mínimo: " + Collections.min(l2));
                break;
            default:
                System.out.println("ERROR - The Warning");
                break;

        }
    }
}
