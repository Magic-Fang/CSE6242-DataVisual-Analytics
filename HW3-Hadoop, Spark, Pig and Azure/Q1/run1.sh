hadoop jar ./target/q1-1.0.jar edu.gatech.cse6242.Q1 ./cse6242/graph1.tsv ./cse6242/q1output1
hadoop fs -getmerge ./cse6242/q1output1/ q1output1.tsv
hadoop fs -rm -r ./cse6242/q1output1
