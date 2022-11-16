## About Kafka
Kafka is a distributed event streaming platform with high throughput, open-sourced by Apache
- As a streaming platform, Kafka is able to handle all streaming requests on the website by consumers, and allow producers to publish events in the meanwhile. From this perspective, Kafka can be seen as a Message Queue Middleware.
- On the other hand, Kafka can persist the streaming it has received and tolerant faults, thanks to its distributed architecture. From this perspective, Kafka can be seen as a NoSQL database.

Our test simulates the two scenarios above.
- It will create a topic with 64 partitions, in which every record is 100 bytes in size.
- Afterwards, 5 producers or consumers are to start in parallel, each adding 10million records to the topic.
- Finally, completion time will be counted to calculate throughput.

Test properties above are set to maximum throughput. If you would like to use your own settings, refer to 
the file server.properties.
## Test Environment
- kafka built from the docker image of ubuntu/kafka:latest, current version is kafka 3.1
- jdk built from dragonwell:11-ubuntu, current version is Alibaba Dragonwell Extended Edition-11.0.16.12+8-GA
## How to run
docker run cape2/kafka
## Analyze Result
Output is like
> write xxxx
>
> read xxxx

Here write means producer test while read means consumer test, followed by the throughput, measured in MB/s.


