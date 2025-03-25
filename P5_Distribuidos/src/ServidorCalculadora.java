import java.lang.reflect.Array;
import java.rmi.RemoteException;
import java.util.ArrayList;

public class ServidorCalculadora implements Calculadora{
    @Override
    public ArrayList<Double> unir(ArrayList<Double> x, ArrayList<Double> y) throws RemoteException{
        ArrayList<Double> unida= new ArrayList<>();
        unida.addAll(x);
        unida.addAll(y);


        return unida;
    }
    @Override
    public String comparacion(ArrayList<Double> x, ArrayList<Double> y){
        if(x.size()>y.size())
        {
            return("La lista 1 es mayor a la lista 2");
        } else if (x.size()<y.size()) {
            return("La lista 2 es mayor a la lista 1");
        }else {
            return("Ambas listas tienen el mismo tamaño");
        }
    }

    @Override
    public ArrayList<Double> alternar(ArrayList<Double> x, ArrayList<Double> y){
        ArrayList<Double>alternada=new ArrayList<>();
        int minSize = Math.min(x.size(), y.size());

        // Alternar elementos hasta el tamaño mínimo de ambas listas
        for (int i = 0; i < minSize; i++) {
            alternada.add(x.get(i));
            alternada.add(y.get(i));
        }

        // Agregar elementos restantes de la lista más larga
        alternada.addAll(x.subList(minSize, x.size()));
        alternada.addAll(y.subList(minSize, y.size()));

        return alternada;
    }
}
