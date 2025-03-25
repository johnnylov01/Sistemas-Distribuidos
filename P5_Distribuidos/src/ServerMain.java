import java.rmi.AlreadyBoundException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
public class ServerMain {
    public static final String UNIQUE_BINDING_NAME = "servidor.Calculadora";
    public static void main(String[] args) throws RemoteException, AlreadyBoundException, InterruptedException {

        final ServidorCalculadora servidor = new ServidorCalculadora();

        final Registry registry = LocateRegistry.createRegistry(2732);

        Remote stub = UnicastRemoteObject.exportObject(servidor, 0);
        registry.bind(UNIQUE_BINDING_NAME, stub);

        Thread.sleep(Integer.MAX_VALUE);

    }

}
