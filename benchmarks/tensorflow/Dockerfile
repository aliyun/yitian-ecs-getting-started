FROM accc-registry.cn-hangzhou.cr.aliyuncs.com/tensorflow/tensorflow:latest

RUN pip3 install --no-cache-dir -i https://pypi.mirrors.ustc.edu.cn/simple Pillow transformers tokenization

WORKDIR /tmp
COPY resnet resnet
COPY ssd ssd
COPY bert bert
COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ./entrypoint.sh
