package org.myorg;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.*;
import java.util.StringTokenizer;
import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import javax.xml.*;
import javax.xml.stream.*;
import java.io.*;
import javax.xml.stream.events.*;
import javax.xml.stream.util.*;
import javax.xml.namespace.QName;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class matchup {

    public static class Batter implements Writable {
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

    public static class Map 
             // extends Mapper<Object, Text, Text, Batter>{
             extends Mapper<Object, Text, Text, Text>{
             public static final Log LOG = LogFactory.getLog(Map.class);
             

            public static ArrayList<String> clusters;

            public void populate(Context context) {
                FSDataInputStream in = null;
                BufferedReader br = null;
                try {
                    FileSystem fs = FileSystem.get(context.getConfiguration());
                    Path path = new Path("clusters.txt");
                    in = fs.open(path);
                    br = new BufferedReader(new InputStreamReader(in));
                } catch (FileNotFoundException e1) {
                    e1.printStackTrace();
                    System.out.println("read from distributed cache: file not found!");
                } catch (IOException e1) {
                    e1.printStackTrace();
                    System.out.println("read from distributed cache: IO Exception");
                }
                try {
                    clusters = new ArrayList<String>();
                    String line = "";
                    while ((line = br.readLine()) != null) {
                        clusters.add(line);
                    }
                } catch (IOException e1) {
                    e1.printStackTrace();
                    System.out.println("read from distributed cache: read length and instances");
                }    
            }

            public void setup(Context context) {
                populate(context);
            }

            public static int containsBatter(String batter, ArrayList<Batter> batterList) {
                int rv = -1;
                for (int i = 0; i < batterList.size(); i++) {
                    if (batterList.get(i).getBatter().equals(batter)) {
                        return i;
                    }
                }
                return rv;
            }
            
            public static void sort_atbat(XMLStreamReader reader, Batter batter) {
                String att = reader.getAttributeValue(null, "event");
                String pitcher = reader.getAttributeValue(null, "pitcher");
                int index = -1;
                int size = clusters.size();
                for (int i = 0; i < size; i++) {
                    String cluster = clusters.get(i);
                    if(cluster.contains(pitcher)) {
                        index = i;
                        break;        
                    }
                }
                if(index == -1) {
                    LOG.info("Pitcher not found");
                }
                else{
                    batter.addData(2*index + 1, 1);
                    batter.incrementTotal(1);
                    if(!att.toLowerCase().contains("out") && !att.contains("DP") && !att.contains("Error")){//if the batter gets a hit
                        batter.addData(2*index, 1);
                    }
                }
                
            }

    public static ArrayList<Batter> parseString(String line, ArrayList<Batter> batterList) {
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
                        }
                        break;
                    case XMLStreamConstants.START_ELEMENT:
                        String tag = reader.getName().toString();
                        if (tag.equals("atbat")) {
                            if (currentElement.equals("")) {
                                currentElement = reader.getAttributeValue(null, "batter");
                            } else {
                                    LOG.info("ERROR ABORT");
                            }
                                
                                int index = containsBatter(currentElement, batterList);                                
                                if ( index == -1) {
                                    batter = new Batter();
                                    int size = clusters.size() * 2;
                                    batter.initArray(size);
                                    batterList.add(batter);
                                    batter.setBatter(currentElement);
                                } else {
                                    batter = batterList.get(index);
                                }
                                    
                                    sort_atbat(reader, batter);
                            } else {
                                batter = new Batter();
                                batter.setBatter(currentElement);
                                batterList.add(batter);
                            }
                        break;
                }
                
            }
            reader.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return batterList;
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
            ArrayList<Batter> batterList = new ArrayList<Batter>();
            batterList = parseString(document, batterList);
            // LOG.info("log thing works");
            context.write(new Text("-1"), new Text(Integer.toString(batterList.size())));
            for (int i = 0; i < batterList.size(); i++) {
                // LOG.info("batterlist is not empty");
                context.write(new Text(Integer.toString(i)), new Text(document));
                // context.write(new Text(batterList.get(i).getBatter()), batterList.get(i));
            }
        }
    }

    
    public static class Reduce 
             extends Reducer<Text,Batter,Text,Batter> {
             // extends Reducer<Text,Value,Text,Text> {

                // @Override

        // This function expects a key of type Text (a word from our document, in this case)
        // and a list of values obtained via iterator (a list of IntWritables, in this case).
        public void reduce(Text key, Iterable<Batter> values, 
                                             Context context
                                             ) throws IOException, InterruptedException {
            Batter rv = new Batter();
            int total = 0;
            for (Batter val : values) {
                int[] data = val.getData();
                if (rv.getTotal() == 0) {
                    rv.initArray(data.length);
                    rv.setBatter(val.getBatter());
                }
                for (int i = 0; i < data.length; i++) {
                    rv.addData(i, data[i]);
                }
                rv.incrementTotal(val.getTotal());
            }
            
            


            // rv.setPitcher("WE ARE HERE");
            
            // Output the results with the same key as the input
            context.write(key, rv);
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
        job.setJarByClass(matchup.class);
        // System.out.println("MARKER");

        // Selects mapper/combiner/reducer
        job.setMapperClass(Map.class);
        //job.setCombinerClass(Reduce.class);
        //job.setReducerClass(Reduce.class);

        // This says that (k1, v1) should be read from text files 
        // and that (k3, v3) should be written to text files 
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        // job.setOutputValueClass(Batter.class);

        // The paths of these input/output are from application arguments
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        // Finally, run the job!
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
