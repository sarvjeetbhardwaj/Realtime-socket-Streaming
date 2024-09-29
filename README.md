# Realtime-socket-Streaming
In this video, you will be building a real-time data streaming pipeline with a dataset of 7 million records. It covers each stage from data acquisition, processing, sentiment analysis with ChatGPT, production to kafka topic and connection to any query engine like elastic search and viaulization tool like powerbi

## TechStack used ::
    - Apache Spark
    - Python
    - TCP/IP Socket
    - Docker
    - Confluent Kafka
    - OpenAI

The project is designed with the following components:
    - Data Source: We use yelp.com dataset for our pipeline.
    - TCP/IP Socket: Used to stream data over the network in chunks
    - Apache Spark: For data processing with its master and worker nodes.
    - Confluent Kafka: Our cluster on the cloud
    - Control Center and Schema Registry: Helps in monitoring and schema management of our Kafka streams.
    - Kafka Connect: For connecting to elasticsearch

## System-Architecture
![alt text](System_architecture.png)

# Steps Followed::
    1. Create src folder , docker-compose.yml , Dockerfile.spark
    2. Create Docker image from docker file -- docker compose up (after cd into src directory)
    3. Download and extract the dataset from yelp.com into datasets folder (inside the src file)
       Please note the data set has not been included due to size limitation.Dataset can be downloaded from yelp.com/datasets
    4. Create streaming-socket.py to stream json data over socket connection the chunks of 2 (This number can be changed).
    5. Create spark-streaming.py to read the streaming data into pyspark
    6. Execute both python files simulataneously to test the streaming results . If this step gives 
    RuntimeError: Java gateway process exited before sending its port number , then execute the following command - sudo apt-get install default-jdk. This install necessary java packages for Pyspark
    7. Set up a Kafka cluster with security credentials and a proper schema registry (schemas folder).Please note that any change in schema has to edited in schema registry in Kafka
    8. Execute the following commands to run the spark-streaming & straming-socket.py within docker containers
        - Enter intercative mode in docker container via - docker exec -it spark-master /bin/bash
        - Execute python3 jobs/streaming-socket.py
        - In different terminal execute the following command  docker exec -it spark-worker spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark-streaming.py
    9. We will see that messages are being sent to Kafka topic
    10. Next step is to perform sentiment analysis using OpenAI Chatgpt.
    11. Create OpenAI chatgpt API credentials
    12. After integrating OpenAI function in the code as shown, make changes to the schema registry in Kafka
    13. Execute step number 8 to run the program.
    14. A new column will be added to data sent to Kafka Topic.
    15. This data can be sent to elasticsearch via Kafka Sink connector and can be used for visualization.(This part has been omitted in the code)