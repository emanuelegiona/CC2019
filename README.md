# CC2019
Project for [Cloud Computing][course] course (A.Y. 2018/2019).

The aim of this project is to familiarize with cloud computing frameworks and SaaS/IaaS services
from the major cloud providers, while studying core concepts of distributed applications.

In particular, the focus is on **load balancing**, **elasticity**, and **resiliency** for what
concerns the infrastructure requirements; the application requirements consist of the ability to
provide a **benchmarking tool**, and again its **elasticity**.

## Implementation details

[Google Cloud Platform][gcp] (and in particular its [Dataproc][dataproc] service) has been used as
cloud provider, due to the ease of cluster and software setup, while the [HDSF Word Count][word_count]
example from the Apache Spark repository has served as the distributed application taking advantage
of the streaming capabilities of Apache Spark.

The Google Cloud Dataproc cluster has been tweaked with autoscaling policies in order to conform to the
infrastructure requirements, while a simple word generator (and a benchmarking routine) have been
developed in order to comply with the application requirements.

Full details available in the [PDF report][report].

## Directory structure

```
- config
    |__ autoscaling_policy.yaml     # GCP autoscaling policy
- data                              # target directory containing files to be processed
    |__ ...
- src                               # source file directory
    |__ benchmark.py                # simulates dynamic application load over time for testing purposes
    |__ file_generator.py           # creates a file then moves it into the target directory
    |__ hdfs_wordcount.py           # streaming Word Count example from Apache Spark
    |__ instance_logger.sh          # BASH script to monitor GCP VM instances over time
- tmp                               # temporary directory for file creation
    |__ ...
- README.md                         # this file
- anonymous_report.pdf              # PDF report
```

For more Apache Spark examples: [Spark website][spark_examples] | [GitHub][spark_github].

[course]: https://sites.google.com/di.uniroma1.it/cloudcomputingcourse/
[gcp]: https://cloud.google.com/
[dataproc]: https://cloud.google.com/dataproc/
[word_count]: https://github.com/apache/spark/blob/master/examples/src/main/python/streaming/hdfs_wordcount.py
[spark_examples]: https://spark.apache.org/examples.html
[spark_github]: https://github.com/apache/spark/tree/master/examples/src/main
[report]: ./anonymous_report.pdf
