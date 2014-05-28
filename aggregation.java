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

public class aggregation {

    public static class Map 
             extends Mapper<Object, Text, IntWritable, Text>{
        
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
            // String line = value.toString();
            String document = value.toString();
            System.out.println("'" + document + "'\n");
            // Iterate over the words of the line and output one (key,
            // value) pair for each word. This task can be optimized
            // by using the StringTokenizer class instead
            // String[] v = line.split(",");
            // String visitor = v[0].trim() + "," + v[1].trim();
            // String visitee = v[19].trim() + "," + v[20].trim();
            
            // int counter1 = 0;
            // int counter2 = 0;
            
            // context.write(new Text(visitor), new MyWritable(1,0)); 
            // context.write(new Text(visitee), new MyWritable(0,1));
            context.write(new IntWritable(0), new Text(document));
        }
    }

    // public static class Combiner
    //          extends Reducer<Text,MyWritable,Text,MyWritable> {
    //     public void reduce(Text key, Iterable<MyWritable> values,
    //                                          Context context
    //                                          ) throws IOException, InterruptedException {
    //         int counter1 = 0;
    //         int counter2 = 0;
    //         for (MyWritable val : values) {
    //             counter1 += val.getCounter1();
    //             counter2 += val.getCounter2();
    //         }
    //         //output
    //         context.write(key, new MyWritable(counter1, counter2));
    //     }
             
    // }
    
    // public static class Reduce 
    //          extends Reducer<Text,MyWritable,Text,MyWritable> {

    //     // This function expects a key of type Text (a word from our document, in this case)
    //     // and a list of values obtained via iterator (a list of IntWritables, in this case).
    //     public void reduce(Text key, Iterable<MyWritable> values, 
    //                                          Context context
    //                                          ) throws IOException, InterruptedException {
    //         int counter1 = 0;
    //         int counter2 = 0;
    //         for (MyWritable val : values) {
    //             counter1 += val.getCounter1();
    //             counter2 += val.getCounter2();
    //         }
            
    //         // Output the results with the same key as the input
    //         if (counter1 > 0 && counter2 >0) {
    //             context.write(key, new MyWritable(counter1, counter2));    
    //         }
    //     }
    // }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: task4 <in> <out>");
            System.exit(2);
        }
        // Creates a MapReduce job and links it to our class
        conf.set("xmlinput.start", "<game>");
        conf.set("xmlinput.end", "</game>");
        Job job = Job.getInstance(conf);
        job.setInputFormatClass(XmlInputFormat.class);
        job.setJarByClass(task4.class);

        // Selects mapper/combiner/reducer
        job.setMapperClass(Map.class);
        // job.setCombinerClass(Combiner.class);
        // job.setReducerClass(Reduce.class);

        // This says that (k1, v1) should be read from text files 
        // and that (k3, v3) should be written to text files 
        job.setOutputKeyClass(Text.class);
        // job.setOutputValueClass(MyWritable.class);

        // The paths of these input/output are from application arguments
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        // Finally, run the job!
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
