package org.myorg;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.*;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
// import org.apache.mahout;
import javax.xml.*;
// import java.io.IOException;
// import java.io.FileReader;
// import java.io.BufferedReader;
import javax.xml.stream.*;
import java.io.*;
import javax.xml.stream.events.*;
import javax.xml.stream.util.*;
import javax.xml.namespace.QName;

public class aggregation {

    public static class Value implements Writable {
        private int total;
        private int handL;
        private int handR;
        private String pitcher;
        private double[][] pitches = new double[11][12];
        
        // public value(){};
        
        public Value(){
            total = 0;
            handL = 0;
            handR = 0;
            pitcher = "";
            for(int i = 0; i < pitches.length; i++) {
                for(int j = 0; j < pitches[0].length; j++) {
                    pitches[i][j] = 0.0;
                }
            }
        }

        public void write(DataOutput out) throws IOException {
            out.writeInt(total);
            out.writeInt(handL);
            out.writeInt(handR);
            out.writeUTF(pitcher);
            for(int i = 0; i < pitches.length; i++) {
                for(int j = 0; j < pitches[0].length; j++) {
                    out.writeDouble(pitches[i][j]);
                }
            }

        }

        public void readFields(DataInput in) throws IOException {
            total = in.readInt();
            handL = in.readInt();
            handR = in.readInt();
            pitcher = in.readUTF();
            pitches = new double[11][12];
            for (int i = 0; i < 11; i++) {
                for (int j = 0; j < 12; j++) {
                    pitches[i][j] = in.readDouble();
                }
            }
        }

        public String toString() {
            return "(pitcher: " + this.pitcher + ")"; 
        }
        
        public void setHand(String h) {
            if(h.equals("L")){
                this.handL = 1;
            }
            else {
                this.handR = 1;
            }
        }

        public void setPitcher(String pitcher) {
            this.pitcher = pitcher;
        }
        
        public void addPitch(int pitch, double[] attr) {
            for(int i = 0; i < attr.length; i++){
                this.pitches[pitch][i] += attr[i];
            }
            this.total++;
        }
        
        public double getAtr(int pitch, int atr) {
            return this.pitches[pitch][atr];
        }

        public void setAtr(int pitch, int atr, double value) {
            this.pitches[pitch][atr] = value;
        }

        public double[] getCol(int i) {
            return this.pitches[i];
        }
        
        public double[][] getPitches(){
            return this.pitches;
        }
        
        public int getTotal(){
            return this.total;
        }
        
        public int getRight() {
            return handR;
        }

        public int getLeft() {
            return handL;
        }      

        public String getPitcher() {
            return this.pitcher;
        }
    }

    public static class Map 
             extends Mapper<Object, Text, Text, Value>{
             // extends Mapper<Object, Text, Text, Text>{

        public static void sort_atbat(String attribute, XMLStreamReader reader, Value pitcher) {
        // System.out.println("[START_ELEMENT] name is: " + reader.getName() + " element text is: " + reader.getAttributeValue(null, attribute)); 
        String att = reader.getAttributeValue(null, attribute);
        if (attribute == "p_throws") {
            pitcher.setHand(att);
            }
        }

    public static void sort_pitch(String attribute, XMLStreamReader reader, Value pitcher) {
        // System.out.println("[START_ELEMENT] name is: " + attribute + ", element text is: " + reader.getAttributeValue(null, attribute)); 
        String[] pitch_attributes = {"break_angle", "break_length", "break_y", "pfx_x", "pfx_z", "spin_dir", "spin_rate", "start_speed", "x0", "y0", "z0"};
        double[] attr = new double[12];
            for (int i = 0; i < pitch_attributes.length; i++) {
                attr[i] = Double.parseDouble(reader.getAttributeValue(null, pitch_attributes[i]));
            }
        attr[pitch_attributes.length] = 1.0;
        if (attribute.equals("FF") || attribute.equals("FA")) {
            pitcher.addPitch(0, attr);
        } else if (attribute.equals("FT")) {
            pitcher.addPitch(1, attr);
        } else if (attribute.equals("FC")) {
            pitcher.addPitch(2, attr);
        } else if (attribute.equals("SI") || attribute.equals("FS")) {
            pitcher.addPitch(3, attr);
        } else if (attribute.equals("SF")) {
            pitcher.addPitch(4, attr);
        } else if (attribute.equals("SL")) {
            pitcher.addPitch(5, attr);
        } else if (attribute.equals("CH")) {
            pitcher.addPitch(6, attr);
        } else if (attribute.equals("CB") || attribute.equals("CU")) {
            pitcher.addPitch(7, attr);
        } else if (attribute.equals("KC")) {
            pitcher.addPitch(8, attr);
        } else if (attribute.equals("KN")) {
            pitcher.addPitch(9, attr);
        } else if (attribute.equals("EP")) {
            pitcher.addPitch(10, attr);
        } else {
            System.out.println("BALL TYPE NOT FOUND");
        }
    }

    public static int containsPitcher(String pitcher, ArrayList<Value> pitcherList) {
        int rv = -1;
        for (int i = 0; i < pitcherList.size(); i++) {
            if (pitcherList.get(i).getPitcher() == pitcher) {
                return i;
            }
        }
        return rv;
    }

    public static ArrayList<Value> parseString(String line, ArrayList<Value> pitcherList) {
        try {
            XMLStreamReader reader = XMLInputFactory.newInstance().createXMLStreamReader(new ByteArrayInputStream(line.getBytes()));
            String propertyName = "";
            String propertyValue = "";
            String currentElement = "";
            Value pitcher = new Value();
            while (reader.hasNext()) {
                int code = reader.next();
                switch (code) {
                    case XMLStreamConstants.END_ELEMENT:
                        if (reader.getName().toString() == "atbat") {
                            currentElement = "";
                        }
                        // System.out.println("[END_ELEMENT] closing tag is: " + reader.getName());
                        break;
                    case XMLStreamConstants.START_ELEMENT:
                        String tag = reader.getName().toString();
                        if (tag.equals("atbat")) {
                            if (currentElement.equals("")) {
                                    currentElement = reader.getAttributeValue(null, "pitcher");
                                } else {
                                    System.out.println("ERROR ABORT");
                                }
                                
                                int index = containsPitcher(currentElement, pitcherList);                                
                                if ( index == -1) {
                                    pitcher = new Value();
                                    pitcherList.add(pitcher);
                                    pitcher.setPitcher(currentElement);
                                } else {
                                    pitcher = pitcherList.get(index);
                                }
                                String[] atbat_attributes = {"pitcher", "p_throws"};
                                for (int i = 0; i < atbat_attributes.length; i++) {
                                    sort_atbat(atbat_attributes[i], reader, pitcher);

                                }
                            } else if (tag.equals("pitch")) {
                                String pitch_type = reader.getAttributeValue(null, "pitch_type");
                                sort_pitch(pitch_type, reader, pitcher);    
                            }
                        
                        
                        break;
                }
                
            }
            reader.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return pitcherList;
    }        

        // @Override
        
        // Mapper function that takes (key, value) and uses the
        // output object to output data. The reporter object can
        // be used report status of the job, we will not be using
        // this feature in this lab.
        public void map(Object key, Text value, Context context
                                        ) throws IOException, InterruptedException {
            // The key here is going to be an unimportant identifier 
            // of the file (of type Object) and the value will a Writable 
            // that contains one line from one input file. To extract 
            // a String object from the Writable, we use toString 
            String document = value.toString();
            ArrayList<Value> pitcherList = new ArrayList<Value>();
            pitcherList = parseString(document, pitcherList);

            for (int i = 0; i < pitcherList.size(); i++) {
                context.write(new Text("pitcher is: " + pitcherList.get(i).getPitcher()), pitcherList.get(i));
            }
        }
    }

    
    public static class Reduce 
             // extends Reducer<Text,Value,Text,Value> {
             extends Reducer<Text,Value,Text,Text> {

                // @Override

        // This function expects a key of type Text (a word from our document, in this case)
        // and a list of values obtained via iterator (a list of IntWritables, in this case).
        public void reduce(Text key, Iterable<Value> values, 
                                             Context context
                                             ) throws IOException, InterruptedException {
            Value rv = new Value();
            int counters[] = new int[11];

            for (Value val : values) {
                if(rv.getRight() == rv.getLeft()){
                    if (val.getRight() == 1) {
                        rv.setHand("R");
                    } else {
                        rv.setHand("L");
                    }
                    rv.setPitcher(val.getPitcher());
                }
                for (int i = 0; i < 11; i++) {
                    counters[i] += val.getAtr(i, 11);
                    rv.addPitch(i, val.getCol(i));
                }
            }

            for (int i = 0; i < 11; i++) {
                if (counters[i] != 0) {
                    System.out.println("MARKER I");
                    for (int j = 0; j < 10; j++) {
                        rv.setAtr(i, j, rv.getAtr(i,j) / counters[i]);
                    }
                }
            }

            rv.setPitcher("WE ARE HERE");
            
            // Output the results with the same key as the input
            context.write(key, new Text("WE ARE HERE"));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: aggregation <in> <out>");
            System.exit(2);
        }
        // Creates a MapReduce job and links it to our class
        // conf.set("xmlinput.start", "<game>");
        // conf.set("xmlinput.end", "</game>");
        Job job = Job.getInstance(conf);
        // job.setInputFormatClass(XmlInputFormat.class);
        job.setJarByClass(aggregation.class);
        // System.out.println("MARKER");

        // Selects mapper/combiner/reducer
        job.setMapperClass(Map.class);
        // job.setCombinerClass(Reduce.class);
        // job.setReducerClass(Reduce.class);

        // This says that (k1, v1) should be read from text files 
        // and that (k3, v3) should be written to text files 
        job.setOutputKeyClass(Text.class);
        // job.setOutputValueClass(Text.class);
        job.setOutputValueClass(Value.class);

        // The paths of these input/output are from application arguments
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        // Finally, run the job!
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
