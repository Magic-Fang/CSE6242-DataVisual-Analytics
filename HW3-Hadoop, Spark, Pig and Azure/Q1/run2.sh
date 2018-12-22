hadoop jar ./target/q1-1.0.jar edu.gatech.cse6242.Q1 ./cse6242/graph2.tsv ./cse6242/q1output2
hadoop fs -getmerge ./cse6242/q1output2/ q1output2.tsv
hadoop fs -rm -r ./cse6242/q1output2
