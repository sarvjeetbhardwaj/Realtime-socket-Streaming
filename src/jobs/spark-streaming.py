from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import from_json,col,udf
from config.config import config
import time
import openai

def sentiment_analysis(comment) -> str:
    if comment:
        openai.api_key = config['openai']['api_key']
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages = [
                {
                    "role": "system",
                    "content": """
                        You're a machine learning model with a task of classifying comments into POSITIVE, NEGATIVE, NEUTRAL.
                        You are to respond with one word from the option specified above, do not add anything else.
                        Here is the comment:
                        
                        {comment}
                    """.format(comment=comment)
                }
            ]
        )
        return completion.choices[0].message['content']
    return "Empty"


def start_streaming(spark:SparkSession):
    topic = 'customer_review'
    while True:
        try:
            stream_df = spark.readStream.format('socket').option('host', '0.0.0.0').option('port', 9999).load()
            
            schema = StructType([
                StructField('review_id',StringType()),
                StructField('user_id',StringType()),
                StructField('business_id',StringType()),
                StructField('stars',FloatType()),
                StructField('date',StringType()),
                StructField('text',StringType())
            ])

            stream_df = stream_df.select(from_json(col('value'),schema=schema).alias('data')).select(('data.*'))

            sentiment_analysis_udf = udf(sentiment_analysis, StringType())

            stream_df = stream_df.withColumn('feedback',
                                             when(col('text').isNotNull(), sentiment_analysis_udf(col('text')))
                                             .otherwise(None)
                                             )

            kafka_df = stream_df.selectExpr('CAST(review_id as STRING) AS key', 'to_json(struct(*)) as value')
            query = (kafka_df.writeStream
                    .format("kafka")
                    .option("kafka.bootstrap.servers", config['kafka']['bootstrap.servers'])
                    .option("kafka.security.protocol", config['kafka']['security.protocol'])
                    .option('kafka.sasl.mechanism', config['kafka']['sasl.mechanisms'])
                    .option('kafka.sasl.jaas.config',
                            'org.apache.kafka.common.security.plain.PlainLoginModule required username="{username}" '
                            'password="{password}";'.format(
                                username=config['kafka']['sasl.username'],
                                password=config['kafka']['sasl.password']
                            ))
                    .option('checkpointLocation', '/tmp/checkpoint')
                    .option('topic', topic)
                    .start()
                    .awaitTermination()
                    )
            
            
            #query = stream_df.writeStream.outputMode('append').format('console').options(truncate=False).start()
            #query.awaitTermination()
        except Exception as e:
            print(f'Exception encountered {e}')
            time.sleep(10)


if __name__ == '__main__':
    spark_conn = SparkSession.builder.appName('SocketStreamConsumer').getOrCreate()

    start_streaming(spark=spark_conn)