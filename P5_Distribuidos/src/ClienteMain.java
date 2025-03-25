import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.ArrayList;
import java.util.Arrays;

public class ClienteMain {
    public static final String UNIQUE_BIDING_NAME="servidor.Calculadora";
    public static void main(String[] args) throws RemoteException, NotBoundException{
        final Registry registry= LocateRegistry.getRegistry(2732);
        Calculadora calculadora=(Calculadora)registry.lookup(UNIQUE_BIDING_NAME);
        ArrayList<Double> lista1 = new ArrayList<>(Arrays.asList(1.1, 3.3, 5.5, 7.7));
        ArrayList<Double> lista2 = new ArrayList<>(Arrays.asList(2.2, 4.4, 6.6));
        ArrayList<Double> unida=calculadora.unir(lista1, lista2);
        System.out.println("Listas unidas"+unida);
    }
}
