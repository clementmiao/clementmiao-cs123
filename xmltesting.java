// package textfiles;

import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;


public class xmltesting {

    public static void parseString(String line) {
        System.out.println(line);
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