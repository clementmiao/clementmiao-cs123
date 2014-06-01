// package textfiles;

import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
import javax.xml.stream.*;
import java.io.*;
import javax.xml.stream.events.*;
import javax.xml.stream.util.*;
import javax.xml.namespace.QName;
import java.util.*;

//CHARACTERS, COMMENT, CDATA, SPACE, ENTITY_REFERENCE, DTD are valid for getText()

public class xmltesting {

    public static class Batter {
        private int total;
        private String batter;
        private int[] data;
        

        public Batter(){
            total = 0;
            batter = "";    
        }

        public Batter(int len){
            total = 0;
            batter = "";
            data = new int[len];
        }

        public void write(DataOutput out) throws IOException {
            out.writeInt(total);
            out.writeUTF(batter);
            out.writeInt(data.length);
            for(int i = 0; i < data.length; i++) {
                out.writeInt(data[i]);    
            }


        }

        public void readFields(DataInput in) throws IOException {
            total = in.readInt();
            batter = in.readUTF();
            int len = in.readInt();
            data = new int[len];
            for (int i = 0; i < len; i++) {
                data[i] = (in.readInt());
            }
        }

        public String toString() {
            String rv = "";
            rv = rv + total;
            for (int i = 0; i < data.length; i++) {
                rv = rv + "," + data[i];
            }
            return rv; 
        }

        public void setTotal(int sum) {
            this.total = sum;
        }
        
        public void incrementTotal(int increment) {
            this.total += increment;
        }

        public void setBatter(String batter) {
            this.batter = batter;
        }

        public void initArray(int n) {
            if (data.length == 0) {
                data = new int[n];
                for (int i = 0; i < n; i++) {
                    data[i] = 0;
                }    
            }
            ;
        }
                
        public int getTotal(){
            return this.total;
        }
        
        public String getBatter() {
            return this.batter;
        }

        public int[] getData() {
            return this.data;
        }

        public void addData(int position, int value) {
            data[position] += value;
        }
    }

    public static void sort_atbat(String attribute, XMLStreamReader reader) {
        System.out.println("[START_ELEMENT] name is: " + reader.getName() + " element text is: " + reader.getAttributeValue(null, attribute)); 
    }

    public static int containsBatter(String batter, ArrayList<Batter> batterList) {
                int rv = -1;
                for (int i = 0; i < batterList.size(); i++) {
                    if (batterList.get(i).getBatter().equals(batter)) {
                        System.out.println("IM HERE");
                        return i;
                    }
                }
                return rv;
        }

    public static void parseString(String line, ArrayList<Batter> batterList) {
        try {
            XMLStreamReader reader = XMLInputFactory.newInstance().createXMLStreamReader(new ByteArrayInputStream(line.getBytes()));
            String currentElement = "";
            Batter batter = new Batter();
            while (reader.hasNext()) {
                int code = reader.next();
                switch (code) {
                    case XMLStreamConstants.END_ELEMENT:
                        if (reader.getName().toString() == "atbat") {
                            currentElement = "";
                            System.out.println("reverted to null");
                        }
                        break;
                    case XMLStreamConstants.START_ELEMENT:
                        String tag = reader.getName().toString();
                        if (tag.equals("atbat")) {
                            System.out.println("at atbat tag");
                            // batter = new Batter();
                            // batter.setBatter(currentElement);
                            // batterList.add(batter);
                            if (currentElement.equals("")) {
                                System.out.println("curent element is empty");
                                currentElement = reader.getAttributeValue(null, "batter");
                            } else {
                                System.out.println("ERROR ABORT");
                                    // LOG.info("ERROR ABORT");
                            }

                            if (currentElement.equals("")) {
                                System.out.println("should have found batter but didn't");
                            }
                                
                                int index = containsBatter(currentElement, batterList);                                
                                if ( index == -1) {
                                    System.out.println("creating batter " + currentElement);
                                    batter = new Batter();
                                    // int size = clusters.size() * 2;
                                    // batter.initArray(size);
                                    batterList.add(batter);
                                    batter.setBatter(currentElement);
                                } else {
                                    System.out.println("found batter in list");
                                    batter = batterList.get(index);
                                }
                                    
                                    // sort_atbat(batter, batter);
                            }
                        break;
                }
                
            }
            reader.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        // return batterList;    
    }

    public static void main(String[] args) throws IOException {
        String file_name = args[0];

        String cluster_file = "clusters.txt";

        try {
            BufferedReader br = new BufferedReader(new FileReader(file_name));
            String line;
            while ((line = br.readLine()) != null) {
                // String document = value.toString();
                ArrayList<Batter> batterList = new ArrayList<Batter>();
                parseString(line, batterList);
                for (int i = 0; i < batterList.size(); i++) {
                    String element = batterList.get(i).getBatter().trim();
                    if (element.equals("")) {
                        System.out.println("element is empty");
                    }
                    System.out.println(batterList.get(i).getBatter().trim());
                     // + '\t' +batterList.get(i));
                }
                System.out.println(batterList.size());
                // System.out.println(line);
                //System.out.println(Arrays.deepToString(line_data));
                // System.out.println(replace(line_data));
            }
            br.close();
        }
        
        catch (IOException e) {
            System.out.println( e.getMessage() );
        }
    }
}