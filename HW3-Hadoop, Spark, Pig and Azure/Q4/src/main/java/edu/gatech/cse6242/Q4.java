package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 
{
public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable>
    {

      private final static IntWritable one = new IntWritable(1);
      private final static IntWritable done = new IntWritable(-1);
      private Text word = new Text();
      private Text word2 = new Text();

      // map function is for --Mapper--, it process line by line
      public void map(Object key, Text value, Context context) 
      throws IOException, InterruptedException 
        {  
          // It then splits the line into tokens separated by whitespaces, 
          // via the StringTokenizer, and emits a key-value pair of < <word>, 1>
          StringTokenizer itr = new StringTokenizer(value.toString());
          int tag = 0;
          while (itr.hasMoreTokens()) 
            {
              if (tag==0){
                word.set(itr.nextToken());
                context.write(word, one);
              }
              else if (tag==1){             
                word2.set(itr.nextToken());
                context.write(word2, done);
              }
              else{
                itr.nextToken();
              }
              tag = tag+1;
            }
        }
    }

  public static class IntSumReducer extends Reducer<Text,IntWritable,Text,IntWritable> 
  {
      private IntWritable result = new IntWritable();

      public void reduce(Text key, Iterable<IntWritable> values, Context context) 
      throws IOException, InterruptedException 
      {
        int sum = 0;
        for (IntWritable val : values) 
        {
          sum = sum+val.get();
        }
        result.set(sum);
        context.write(key, result);
      }
  }


  // ----------------------------- MapReduce 2 -----------------------------------

  public static class TokenizerMapper2 extends Mapper<Object, Text, Text, IntWritable>
    {

      private final static IntWritable one = new IntWritable(1);
      private Text word = new Text();
     
      public void map(Object key, Text value, Context context) 
      throws IOException, InterruptedException 
        {  
          String [] lines = value.toString().split("\t");
            if(lines.length == 2){
                word.set(lines[1]);
                context.write(word, one);
            }
    
        }
    }

    public static class IntSumReducer2 extends Reducer<Text,IntWritable,Text,IntWritable> 
  {
      private IntWritable result = new IntWritable();

      public void reduce(Text key, Iterable<IntWritable> values, Context context) 
      throws IOException, InterruptedException 
      {
        int sum = 0;
        for (IntWritable val : values) 
        {
          sum = sum+val.get();
        }
        result.set(sum);
        context.write(key, result);
      }
  }


// ------------------------------ Impelement -------------------------------------


  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "MR1");

    /* TODO: Needs to be implemented */
    job.setJarByClass(Q4.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path("tmp"));


    job.waitForCompletion(true);
    Job job2 = Job.getInstance(conf, "MR2");
    job2.setJarByClass(Q4.class);
    job2.setMapperClass(TokenizerMapper2.class);
    job2.setCombinerClass(IntSumReducer2.class);
    job2.setReducerClass(IntSumReducer2.class);
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);


    FileInputFormat.addInputPath(job2, new Path("tmp"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    //FileSystem.delete(Path "tmp", boolean recursive);

    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }
}
