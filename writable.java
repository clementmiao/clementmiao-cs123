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

public class task3 {
    public static class MyWritable implements Writable {
        private int counter1;
        private int counter2;

        public MyWritable(){};

        public MyWritable(int inCounter1, int inCounter2) {
            counter1 = inCounter1;
            counter2 = inCounter2;
        };

        public int getCounter1(){
            return counter1;
        };

        public int getCounter2(){
            return counter2;
        };

        public void write(DataOutput out) throws IOException {
            out.writeInt(counter1);
            out.writeInt(counter2);
        };

        public void readFields(DataInput in) throws IOException {
            counter1 = in.readInt();
            counter2 = in.readInt();
        }

        public String toString() {
            return "("+this.counter1+","+this.counter2+")";
        }
    }

    public static class Map 
             extends Mapper<Object, Text, Text, MyWritable>{
        
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
            String line = value.toString();

            
            String[] v = line.split(",");
            String name = v[0].trim() + "," + v[1].trim();
            String full_date = v[11];
            String[] arr = full_date.split("\\s+");
            
            int counter1 = 0;
            int counter2 = 0;
            
            int year_num = 0;
            if (arr.length == 2) {
                String date_string = arr[0];
                String[] date_array = date_string.split("/");
                if (date_array.length == 3) {
                    String year = date_array[2];
                    year_num = Integer.parseInt(year);
                }
            }
            if (year_num == 2009) {
                counter1 = 1;
            } else if (year_num == 2010) {
                counter2 = 1;
            }


            MyWritable tuple = new MyWritable(counter1, counter2);
            context.write(new Text(name), tuple); 
        }
    }

    public static class Combiner
             extends Reducer<Text,MyWritable,Text,MyWritable> {
        public void reduce(Text key, Iterable<MyWritable> values,
                                             Context context
                                             ) throws IOException, InterruptedException {
            int counter1 = 0;
            int counter2 = 0;
            for (MyWritable val : values) {
                counter1 += val.getCounter1();
                counter2 += val.getCounter2();
            }
            //output
            context.write(key, new MyWritable(counter1, counter2));
        }
             
    }
    
    public static class Reduce 
             extends Reducer<Text,MyWritable,Text,MyWritable> {

        // This function expects a key of type Text (a word from our document, in this case)
        // and a list of values obtained via iterator (a list of IntWritables, in this case).
        public void reduce(Text key, Iterable<MyWritable> values, 
                                             Context context
                                             ) throws IOException, InterruptedException {
            int counter1 = 0;
            int counter2 = 0;
            for (MyWritable val : values) {
                counter1 += val.getCounter1();
                counter2 += val.getCounter2();
            }
            
            // Output the results with the same key as the input
            if (counter1 > 0 && counter2 >0) {
                context.write(key, new MyWritable(counter1, counter2));    
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
        job.setJarByClass(task3.class);

        // Selects mapper/combiner/reducer
        job.setMapperClass(Map.class);
        job.setCombinerClass(Combiner.class);
        job.setReducerClass(Reduce.class);

        // This says that (k1, v1) should be read from text files 
        // and that (k3, v3) should be written to text files 
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(MyWritable.class);

        // The paths of these input/output are from application arguments
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        // Finally, run the job!
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
