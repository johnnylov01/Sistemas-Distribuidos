import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.ArrayList;

public interface Calculadora extends Remote{
    ArrayList<Double> unir(ArrayList<Double> x, ArrayList<Double> y) throws RemoteException;
    String comparacion(ArrayList<Double> x, ArrayList<Double> y) throws RemoteException;
    ArrayList<Double> alternar(ArrayList<Double> x, ArrayList<Double> y) throws RemoteException;
}
