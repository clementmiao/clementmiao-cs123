package org.myorg;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.*;
import java.util.StringTokenizer;
import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.*;
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

public class test {

    public static class Map 
             extends Mapper<Object, Text, Text, Text>{

            public ArrayList<String> clusters;

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
            String useless_line = value.toString(); 
            for (int i = 0; i < clusters.size(); i++) {
                context.write(new Text("cluster is:"), new Text(clusters.get(i)));
            }

             
        }
    }


    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: task3 <in> <out>");
            System.exit(2);
        }
        // Creates a MapReduce job and links it to our class
        Job job = Job.getInstance(conf);
        job.setJarByClass(test.class);

        // Selects mapper/combiner/reducer
        job.setMapperClass(Map.class);
        // job.setCombinerClass(Combiner.class);
        // job.setReducerClass(Reduce.class);

        // This says that (k1, v1) should be read from text files 
        // and that (k3, v3) should be written to text files 
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        // The paths of these input/output are from application arguments
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        // Finally, run the job!
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
