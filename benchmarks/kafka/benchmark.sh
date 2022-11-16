bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
bin/kafka-server-start.sh -daemon config/server.properties
sleep 10s

bin/kafka-topics.sh --create --topic testTopic --bootstrap-server 127.0.0.1:9092 --partitions 64 > /dev/null 2>&1

producer_ite=5
for i in `seq $producer_ite`
do
  bin/kafka-producer-perf-test.sh --topic testTopic --num-records 10000000 --throughput -1  --record-size 100  --producer-props bootstrap.servers=127.0.0.1:9092 acks=1  buffer.memory=67108864 batch.size=65536  linger.ms=3 > producer_log$i &
done
sleep 1m

consumer_ite=5
for i in `seq $consumer_ite`
do
  bin/kafka-consumer-perf-test.sh --topic testTopic --messages 10000000 --bootstrap-server 127.0.0.1:9092 --threads 10 --timeout 6000000 > consumer_log$i &
done
sleep 1m

write_sum=0.0
read_sum=0.0
for i in `seq $producer_ite`
do
  write_thr=$(cat producer_log$i | grep 99th | awk '{print substr($6,2)}')
  write_sum=$(echo $write_sum $write_thr | awk '{print $1+$2}')
done
for i in `seq $consumer_ite`
do
  read_thr=$(cat consumer_log$i | grep 2022- | awk -F, '{print substr($4,2)}')
  read_sum=$(echo $read_sum $read_thr | awk '{print $1+$2}')
done
echo $write_sum $producer_ite | awk '{print "write",$1/$2}'
echo $read_sum $consumer_ite | awk '{print "read",$1/$2}'
