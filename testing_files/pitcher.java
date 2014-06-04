package org.myorg;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.*;
import java.text.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

public class Pitchers {

    public static class value {
        private int total;
        private int handL;
        private int handR;
        private double[][] pitches = new double[11][12];
        
        
        public value() {
            total = 0;
            handL = 0;
            handR = 0;
            for(int i = 0; i < pitches.length; i++) {
                for(int j = 0; j < pitches[0].length; j++) {
                    pitches[i][j] = 0.0;
                }
            }
        }
        
        public void setHand(String h) {
            if(h.equals("L"){
                this.handL = 1;
            }
            else {
                this.handR = 1;
            }
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
        
        public double[][] getPitches(){
            return this.pitches;
        }
        
        public int getTotal(){
            return this.total;
        }
        
        public boolean isRight() {
            return (handR == 1);
        }      
    }
    public static class Map extends MapReduceBase 
                            implements Mapper<LongWritable, Text, Text, IntWritable> {

        public void map(LongWritable key, 
                        Text value, 
                        OutputCollector<Text, IntWritable> output, 
                        Reporter reporter) throws IOException {

            String svalue = value.toString();
            String[] line = svalue.split(",");
            String lastname = line[0];
            String firstname = line[1];
            DateFormat df = new SimpleDateFormat("M/d/yyyy hh:mm");
            df.setLenient(false);
            Calendar c = Calendar.getInstance();
            try {
		c.setTime(df.parse(line[11]));
	    }
	    catch (ParseException e) {}
            output.collect(new Text(firstname + " " + lastname), new IntWritable(c.get(Calendar.YEAR)));
        }
    }


    public static class Reduce extends MapReduceBase 
                               implements Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, 
                           Iterator<IntWritable> values, 
                           OutputCollector<Text, IntWritable> output, 
                           Reporter reporter) throws IOException {
            
            yearTrack dude = new yearTrack();
            // values.hasNext() returns true when the iterator is not
            // empty.
            IntWritable value;
            while (values.hasNext()) {
                // Fetches the next year value
                value = values.next();

                //if in 2009 or 2010, updates values accordingly
                if(value.get() == 2009) {
                    dude.yesNine();
                }
                else if(value.get() == 2010) {
                    dude.yesTen();
                }
            }
	    
	        if (dude.both()){
            // Output the results with the same key as the input
		    output.collect(key, new IntWritable(0));
	        }
	    }
    }


    public static void main(String[] args) throws Exception {
        // Creates a MapReduce job and links it to our class
        JobConf conf = new JobConf(Task3.class);
        conf.setJobName("task3");

        // Specifies (k3, v3) as (string, int)
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(IntWritable.class);

        // Selects mapper/combiner/reducer
        conf.setMapperClass(Map.class);
	// conf.setCombinerClass(Reduce.class);
        conf.setReducerClass(Reduce.class);

        // This says that (k1, v1) should be read from text files 
        // and that (k3, v3) should be written to text files 
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        // The paths of these input/output are from application arguments
        FileInputFormat.setInputPaths(conf, new Path(args[0]));
        FileOutputFormat.setOutputPath(conf, new Path(args[1]));

        // Finally, run the job!
        JobClient.runJob(conf);
    }
}
