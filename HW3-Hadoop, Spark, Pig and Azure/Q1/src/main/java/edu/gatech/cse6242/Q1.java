package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1{

public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable>
    {

      private final static IntWritable one = new IntWritable(1);
      private Text word = new Text();
      //private IntWritable word2 = new IntWritable();

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
              }
              //System.out.println("here");
              else if (tag==2){
                IntWritable word2 = new IntWritable(Integer.parseInt(itr.nextToken()));
                //word2.set(Integer.parseInt(itr.nextToken()));
                
                //System.out.println(word);
                //System.out.println(word2);
                //System.out.println("--------");
                
                context.write(word, word2); 
                //context.write(word, one);
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
          sum = Math.max(val.get(), sum);
        }
        result.set(sum);
        context.write(key, result);
      }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    /* TODO: Needs to be implemented */
    job.setJarByClass(Q1.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
