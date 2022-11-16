FROM dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:11-ubuntu as jdk

FROM ubuntu/kafka
WORKDIR /opt/kafka/
COPY --from=jdk /opt/java/openjdk jdk
COPY server.properties config/server.properties
COPY benchmark.sh benchmark.sh
RUN export JAVA_HOME=/opt/kafka/jdk/;export PATH=/opt/kafka/jdk/bin/:$PATH
ENTRYPOINT /usr/bin/bash benchmark.sh
