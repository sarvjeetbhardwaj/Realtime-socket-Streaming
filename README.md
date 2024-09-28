# Realtime-socket-Streaming
In this video, you will be building a real-time data streaming pipeline with a dataset of 7 million records. It covers each stage from data acquisition, processing, sentiment analysis with ChatGPT, production to kafka topic and connection to elasticsearch.

TechStack used ::
    - Apache Spark
    - Python
    - TCP/IP Socket
    - Docker
    - Elasticsearch
    - Confluent Kafka
    - OpenAI

The project is designed with the following components:
    - Data Source: We use yelp.com dataset for our pipeline.
    - TCP/IP Socket: Used to stream data over the network in chunks
    - Apache Spark: For data processing with its master and worker nodes.
    - Confluent Kafka: Our cluster on the cloud
    - Control Center and Schema Registry: Helps in monitoring and schema management of our Kafka streams.
    - Kafka Connect: For connecting to elasticsearch
    - Elasticsearch: For indexing and querying

## System-Architecture
![alt text](System_architecture.png)

# Steps Followed::
    1. Create src folder , docker-compose.yml , Dockerfile.spark
    2. Create Docker image from docker file -- docker compose up (after cd into src directory)
    3. Download and extract the dataset from yelp.com into datasets folder (inside the src file)
       Please note the data set has not been included due to size limitation
