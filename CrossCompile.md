# 1 环境配置
## 1.1 系统环境
本文使用的环境如下
机器：ecs.ebmg6.26xlarge （裸金属实例）
系统：Anolis 8.8 （推荐使用）
## 1.2 安装 docker / buildx
```bash
[root@anolis88 ~]# yum install docker -y
...
[root@anolis88 ~]# docker ps
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
CONTAINER ID  IMAGE       COMMAND     CREATED     STATUS      PORTS       NAMES
[root@anoli88 ~]# docker buildx --help
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Build images

Description:
  Build images

Usage:
  podman buildx [command]

Aliases:
  buildx, builder

Available Commands:
  build       Build an image using instructions from Containerfiles
  prune       Remove unused images
```
安装成功，buildx 也安装成功，而且还帮你启动了
## 1.3 注册 binfmt 
如果不注册 binfmt 将无法运行 arm 架构容器：
```bash
# host 机器架构是 x86
[root@anolis88 ~]# arch
x86_64
# arm 架构容器报错无法运行
[root@iZbp13q2r2hxjydk03obwiZ ~]# docker run --rm -t openanolis/anolisos:8.6-aarch64 arch
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
exec /usr/bin/arch: exec format error
```
注册 binfmt 的方法：
```bash
[root@anolis88 ~]# echo ":qemu-aarch64:M::\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7\x00:\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff:/usr/bin/qemu-aarch64-static:" > /etc/binfmt.d/qemu-aarch64-static.conf
[root@anolis88 ~]# systemctl restart systemd-binfmt.service
[root@anolis88 ~]# cat /proc/sys/fs/binfmt_misc/qemu-aarch64
enabled
interpreter /usr/bin/qemu-aarch64-static
flags: F
offset 0
magic 7f454c460201010000000000000000000200b700
mask ffffffffffffff00fffffffffffffffffeffffff
```
# <a name="Zt8Or"></a>2 跨架构镜像构建
## 2.1 获取 qemu-aarch64-static
```bash
# 安装 qemu-user-static
[root@anolis88 ~]# yum install qemu-user-static
# 拷贝到工作目录
[root@anolis88 ~]# cp /usr/bin/qemu-aarch64-static ./
```
安装 qemu-user-static ，其中包含了可执行文件 qemu-aarch64-static，该二进制文件用于在其他平台模拟 aarch64。并将 qemu-aarch64-static 拷贝到工作目录。
## 2.2 创建 Dockerfile
这里拉取官方维护的 Anolis 8.6 镜像（8.8 的 docker 镜像暂未发布），拷贝 qemu-aarch64-static ，安装必要的工具和依赖。（以下是推荐的 Dockerfile，可根据需要增加或减少 yum install 的内容）
```bash
[root@anolis88 ~]# cat > Dockerfile <<EOF
FROM --platform=$TARGETPLATFORM openanolis/anolisos:8.6-aarch64
COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static
USER root
RUN yum install -y wget autoconf automake libtool make gcc.aarch64 pcre pcre-devel zlib-devel gd-devel libxslt-devel openssl-devel perl-devel perl java-1.8.0-openjdk-devel.aarch64 maven.noarch
EOF
```
## 2.3 创建镜像
Dockerfile + qemu-aarch64-static 准备好后，就可以开始镜像构建：
```bash
# build 镜像
[root@anoli88 ~]# docker buildx build -t arm-on-x86/ax:1 .
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
STEP 1/2: FROM openanolis/anolisos:8.6-aarch64
✔ docker.io/openanolis/anolisos:8.6-aarch64
Trying to pull docker.io/openanolis/anolisos:8.6-aarch64...
Getting image source signatures
Copying blob 3379616b4530 done
Copying config 8571375fbd done
Writing manifest to image destination
Storing signatures
STEP 2/2: COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static
COMMIT arm-on-x86/ax:1
--> f1eba2a31dc
Successfully tagged localhost/arm-on-x86/ax:1
f1eba2a31dcf21a44cd513889b1e65e48f13ae2e3e4d9d2da9595d22967628d7

# 测试容器
[root@anoli88 ~]# docker run -t --rm --privileged arm-on-x86/ax:1 arch
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
aarch64
```
至此，一个跨架构镜像构建成功，后面可以使用这个镜像来编译你需要的应用，比如 [3.1 C 语言应用构建](#aHmwv)；当然，[3](#owqHK) 中还提供了其他语言应用的构建例子。
# <a name="owqHK"></a>3 跨架构多语言镜像使用
基于Alinux3的语言基础镜像主要能在以下两个方面提供支持。首先，在ECS官方制品中心上缺少语言镜像，用户可能使用dockerhub/ghcr.io上的社区镜像构建应用，但缺少官方支持和安全更新。为此，我们在制品中心发布了经过ECS认证的语言镜像，为用户提供可靠的基础镜像。其次，这些镜像会进行ECS环境优化，用户可以无缝迁移至倚天平台并获得性能收益。
本文档针对支持的语言提供了语言镜像的使用说明和迁移指南。
## <a name="aHmwv"></a>3.1 C
使用 [2](#Zt8Or) 中构建出来的容器编译并运行 nginx（aarch64 版本）
```shell
# 进入容器
[root@anolis88 ~]# docker run -it --rm --privileged arm-on-x86/ax:1  /bin/bash
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
[root@2eccae6011ea /]#

# 下载/解压/编译/安装 Nginx
[root@2eccae6011ea /]# wget http://nginx.org/download/nginx-1.20.1.tar.gz
[root@2eccae6011ea /]# tar xf nginx-1.20.1.tar.gz
[root@2eccae6011ea /]# cd nginx-1.20.1
[root@2eccae6011ea nginx-1.20.1]# ./configure
[root@2eccae6011ea nginx-1.20.1]# make -j

# 查看 Nginx 二进制文件为 ARM aarch64 格式
[root@2eccae6011ea nginx-1.20.1]# file objs/nginx
objs/nginx: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, BuildID[sha1]=10389dc40e27c55faea46a2c2b6994baa335c0a9, with debug_info, not stripped

# 安装 Nginx
[root@2eccae6011ea nginx-1.20.1]# make install -j

# 启动 Nginx
[root@2eccae6011ea nginx-1.20.1]# /usr/local/nginx/sbin/nginx &

# 查看是否启动成功
[root@2eccae6011ea nginx-1.20.1]# ps aux | grep nginx
root       15241  0.0  0.0 230080 10520 ?        Ssl  08:07   0:00 /usr/bin/qemu-aarch64-static /usr/local/nginx/sbin/nginx
nobody     15243  0.0  0.0 233988 12724 ?        Sl   08:07   0:00 /usr/bin/qemu-aarch64-static /usr/local/nginx/sbin/nginx
root       57296  0.0  0.0 228420  9324 pts/0    Sl+  09:27   0:00 /usr/bin/qemu-aarch64-static /usr/bin/grep --color=auto nginx
[root@2eccae6011ea nginx-1.20.1]# curl localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
```
## 3.2 C++
创建 Dockerfile，需添加安装必要的工具和依赖（包含gcc 11）
```shell
FROM    --platform=$TARGETPLATFORM openanolis/anolisos:8.6-aarch64
COPY    qemu-aarch64-static /usr/bin/qemu-aarch64-static
USER    root
RUN     yum install -y wget autoconf automake libtool make gcc pcre pcre-devel \
        zlib-devel gd-devel libxslt-devel openssl-devel perl-devel perl \ 
        java-1.8.0-openjdk-devel maven.noarch git git-lfs gcc-c++ cmake \
        libdwarf-devel libzstd-devel diffutils libstdc++-static flex byacc vim
RUN     yum install gcc-toolset-11-gcc gcc-toolset-11-gcc-c++ -y && \ 
        sed -i '$a\source /opt/rh/gcc-toolset-11/enable' /root/.bashrc && \
        source /root/.bashrc
```
编译并测试[雅兰亭库](https://github.com/alibaba/yalantinglibs)，该库是一个c++20 基础库，里面包括了序列化库、rpc库、协程库、日志库等等，帮助c++ 用户快速构建高性能c++ 应用。
```shell
# 进入容器
docker buildx build -t cross-compile-cpp:v1 .
docker run -it --rm --privileged cross-compile-cpp:v1 bash

# clone/build/test/install 雅兰亭库
git clone https://github.com/alibaba/yalantinglibs.git
cd yalantinglibs
mkdir build && cd build
cmake .. 
make -j
make install

# 测试 雅兰亭库
make test

# 验证编译产物是aarch64格式的可执行文件
cd tests
file test_connection 
```
## 3.3 Go
提供了基于Alinux3的Go构建镜像，支持在x86平台上构建x86和aarch64的go应用。

以开源git服务应用gogs为例说明跨架构go镜像的使用方式。

在如下dockerfile中，首先在构建镜像中拉取代码并构建可执行文件，随后将可执行文件复制到精简的alinux3环境中。根据构建时不同的参数，该dockerfile可无需修改内容生成支持x86和aarch64架构的应用镜像。

构建参数：docker buildx build --platform=linux/amd64或docker buildx build --platform=linux/arm64
```shell
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/golang:1.19.4 as builder

RUN yum install -y git && git clone https://github.com/gogs/gogs.git

WORKDIR /gogs

RUN go build .

FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/alinux3:latest

COPY --from=builder /gogs/gogs /gogs

ENTRYPOINT [ "/gogs" ]
```
构建完成后可使用docker run命令验证镜像可用。
## 3.4 Java
制品中心提供了基于Dragonwell的多架构镜像。

以Java Web应用spring-petclinic为例说明跨架构Java（Dragonwell）镜像的使用方式。

基于跨架构的dragonwell镜像构建的应用镜像无需修改，使用不同的构建参数能得到x86和aarch64架构的应用镜像。

构建参数：docker build --platform=linux/amd64或docker build --platform=linux/arm64
```shell
FROM dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell as builder

RUN yum install -y git && git clone https://github.com/spring-projects/spring-petclinic.git

WORKDIR /spring-petclinic

RUN ./mvnw package

ENTRYPOINT [ "bash", "-c", "java -jar target/*.jar" ]

```
构建完成后可使用docker run命令验证镜像可用。
## 3.5 Python
提供了基于Alinux3的Python镜像，目前提供了Python 3.11的语言基础镜像。同时由于Tensorflow 1.15使用较广且社区没有已有的arm版本，也提供了Python 3.6 + Tensorflow 1.15的镜像。

以基于flask的web应用说明Python镜像的使用方式。

基于跨架构的Python镜像构建的应用镜像无需修改，使用不同的构建参数能得到x86和aarch64架构的应用镜像。

构建参数：docker build --platform=linux/amd64或docker build --platform=linux/arm64
```shell
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

RUN yum install -y git libpq-devel && git clone https://github.com/mjhea0/flaskr-tdd.git

WORKDIR /flaskr-tdd

RUN bash -c 'echo "SQLAlchemy<2" >> requirements.txt'
RUN python3 -m pip install -r requirements.txt

ENV FLASK_APP=project/app.py

ENTRYPOINT [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000", "--debugger" ]
```
构建完成后可使用docker run命令验证镜像可用。
Tensorflow镜像地址位于alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/language-containers/tensorflow:1.15.5，使用方式类似，需要在构建时基于该镜像，并按需部署应用。
## 3.6 Node.js
提供了基于Alinux3的Node.js镜像，镜像基于Noslate Node.js发行版。

以基于nextjs的web应用说明Node.js镜像的使用方式。

首先创建模版项目：
```shell
npm init -y vite-plugin-ssr
```
随后基于本地代码构建应用镜像：
```shell
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/node:16.17.1-nslt

COPY --chown=node vite-ssr-project /nodejs-vitest
WORKDIR /nodejs-vitest

RUN yarn install

ENTRYPOINT [ "npm", "run", "dev" ]
```
构建完成后可使用docker run命令验证镜像可用。

