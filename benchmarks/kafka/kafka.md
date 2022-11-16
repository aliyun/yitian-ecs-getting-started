## 关于kafka
Kafka是由Apache开源的一个高吞吐量的分布式发布订阅消息系统。
- 作为一个流处理平台，Kafka可以处理消费者在网站中的所有动作流数据，同时允许生产者发布记录流。在这方面，它类似于一个消息队列中间件。
- 同时，Kafka能够持久化收到的记录流，其分布式的结构具有容错能力。在这方面，它类似于一个非关系型数据库。  
  
我们的测试模拟了以上两个场景。
- 它会建立一个具有64分区的记录流，其中的每条记录大小为100字节。
- 之后并行启动5个生产者或消费者，向记录流中添加或查询10M条记录。
- 最后统计所有记录的完成时间，计算吞吐量。

以上配置已调整到最大化吞吐量的状态。如需自定义测试配置，可修改server.properties文件
## 测试环境
- kafka来自ubuntu/kafka:latest镜像，当前版本为kafka 3.1
- jdk来自dragonwell:11-ubuntu镜像，当前版本为Alibaba Dragonwell Extended Edition-11.0.16.12+8-GA
## 运行方法
docker run cape2/kafka
## 结果解析
此测试的输出类似于
> write xxxx
> 
> read xxxx

write为写测试结果，read为读测试结果。数字为分数，单位是MB/s，越高越好


