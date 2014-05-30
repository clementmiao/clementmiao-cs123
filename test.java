import java.util.*;


public class test {
    
    public static void addElement(ArrayList list) {
        list.add(21);
    }

    public static void main(String[] args) throws Exception {
        ArrayList list = new ArrayList();
        list.add(1);
        addElement(list);
        list.add(3);
        addElement(list);
        for (int i = 0; i < list.size(); i++)
            System.out.println(list.get(i));

}    
}

