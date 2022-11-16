FROM ubuntu

WORKDIR /benchmark

RUN sed -i -E 's/(security|archive|ports).ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt install -y libopenblas-base python3 python3-numpy &&  rm -rf /var/lib/apt/lists/
COPY benchmark.py benchmark.py

ENTRYPOINT python3 benchmark.py
