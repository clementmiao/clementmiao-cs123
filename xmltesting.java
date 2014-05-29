// package textfiles;

import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
import javax.xml.stream.*;
import java.io.*;
import javax.xml.stream.events.*;
import javax.xml.stream.util.*;
import javax.xml.namespace.QName;

//CHARACTERS, COMMENT, CDATA, SPACE, ENTITY_REFERENCE, DTD are valid for getText()

public class xmltesting {

    public static void parseString(String line) {
        // System.out.println(line);
        try {
            XMLStreamReader reader = XMLInputFactory.newInstance().createXMLStreamReader(new ByteArrayInputStream(line.getBytes()));
            String propertyName = "";
            String propertyValue = "";
            String currentElement = "";
            while (reader.hasNext()) {
                int code = reader.next();
                // System.out.println("reader element is :" + reader.getLocalName());
                switch (code) {
                    case XMLStreamConstants.CHARACTERS:
                        System.out.println("[CHARACTERS] reader text is: " + reader.getText());
                        break;
                    case XMLStreamConstants.END_ELEMENT:
                        break;
                    case XMLStreamConstants.COMMENT:
                        System.out.println("[COMMENT] reader text is: " + reader.getText());
                        break;
                    case XMLStreamConstants.CDATA:
                        System.out.println("[CDATA] reader text is: " + reader.getText());
                        break;
                    case XMLStreamConstants.SPACE:
                        System.out.println("[SPACE] reader text is: " + reader.getText());
                        break;
                    case XMLStreamConstants.ENTITY_REFERENCE:
                        System.out.println("[ENTITY_REFERENCE] reader text is: " + reader.getText());
                        break;
                    case XMLStreamConstants.DTD:
                        System.out.println("[DTD] reader text is: " + reader.getText());
                        break;
                    case XMLStreamConstants.START_ELEMENT:
                        System.out.println("[START_ELEMENT] name is: " + reader.getName() + " element text is: " + reader.getAttributeValue(null, "hole"));
                        break;
                    default:
                        // System.out.println("reader text is: " + reader.getText());    

                }
                

                
            }
            reader.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void main(String[] args) throws IOException {
        String file_name = args[0];

        try {
            BufferedReader br = new BufferedReader(new FileReader(file_name));
            String line;
            while ((line = br.readLine()) != null) {
                parseString(line);
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