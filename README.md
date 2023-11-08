# 倚天云服务器技术指南

此项目为倚天云服务器的技术指南，介绍基于倚天710芯片的云服务器的基本情况，并提供资源帮助使用者和开发者快速上手。无论您是想了解倚天云服务器，或是进行不同实例间性能比较，还是准备将您的应用迁移到ARM平台都可以在这个项目中获得有用的信息。另外欢迎大家将自己的使用经验贡献出来，帮助其他开发者更好的使用倚天云服务器。

# 主要内容
* [迁移到倚天](#迁移到倚天)
* [编译构建适用于倚天的版本](#编译构建适用于倚天的版本)
   - [跨架构构建指引](CrossCompile.md)
* [倚天上的性能优化](#倚天上的性能优化)
* 编程语言层面迁移及优化建议
   - [C++](Languages/C++.md)
   - [Java](Languages/Java.md)
   - [Python](Languages/Python.md)
   - [NodeJS](Languages/NodeJS.md)
* [容器镜像和容器服务]
   - [容器镜像](container/ACR.md)
   - [容器服务](container/ACK.md)
   - [构建多架构镜像](container/README.md)
* [倚天基础库最佳实践](#倚天基础库最佳实践)
* [倚天PaaS最佳实践](#倚天paas最佳实践)
* [操作系统支持](#操作系统)
* [倚天云服务器基本信息](#倚天云服务器基本信息)
* [基准测试程序](#基准测试程序)
* [推荐软件版本](README.md#推荐软件版本)
* [资源下载](#资源下载)
* 实用工具
   - [智能化性能调优工具Keentune](Keentune.md)
   - [Java诊断工具Eclipse Jifa](Jifa.md)
   - [Java版本升级工具Eclipse Migration Toolkit for Java](EMT4J.md)

# 迁移到倚天
   - [EasyYitian工具介绍](EasyYitian/README.md)
# 编译构建适用于倚天的版本

# 倚天上的性能优化

# 倚天基础库最佳实践

# 倚天PaaS最佳实践

# 倚天云服务器基本信息
请访问[阿里云倚天云服务器官方页面](https://www.aliyun.com/product/ecs/yitian)获取相关信息

# 基准测试程序
此项目中集成了大量典型基准测试程序，您可以使用这些测试轻松的对不同平台的性能进行比较。 目前集成的测试有三大特点：

   - 可以跨架构运行。这些测试无论是在X86还是ARM架构平台上都可以运行
   - 通过docker固化了软件环境
   - 可以一键运行

请访问[基准测试介绍](benchmarks/benchmarks.md)获取测试信息及docker安装方法，具体包括：

   - [kafka](benchmarks/kafka/kafka.md)
   - [openblas](benchmarks/openblas/openblas.md)
   - [php](benchmarks/php/php.md)
   - [tensorflow](benchmarks/tensorflow/tensorflow.md)
   - [web-tooling](benchmarks/web-tooling-benchmark/web-tooling.md)

# 操作系统
倚天云服务目前支持的部分操作系统如下表所示，您可以在创建云服务器的时候通过选择公共镜像使用OS。

推荐使用由阿里云官方发布的[Alibaba Cloud Linux 3](os.md)，在全面兼容CentOS/RHEL生态的同时，与阿里云基础设施做了深度优化，为实例提供专项的性能和稳定性优化，并提供完善的生态支持，同时用户还可以免费享受阿里云提供的全生命周期服务保障

<table>
   <tr>
      <td>操作系统</td>
      <td>版本</td>
   </tr>
   <tr>
      <td>Alibaba Cloud Linux</td>
      <td>3.2104 LTS 64位 ARM版</td>
   </tr>
   <tr>
      <td rowspan="10">Anolis OS</td>
      <td>8.6 RHCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>8.6 ANCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>8.4 RHCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>8.4 ANCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>8.2 RHCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>8.2 ANCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>7.9 RHCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>7.9 ANCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>7.7 RHCK 64位 ARM版</td>
   </tr>
   <tr>
      <td>7.7 ANCK 64位 ARM版</td>
   </tr>
   <tr>
      <td rowspan="2">CentOS</td>
      <td>8.4 64位 ARM版</td>
   </tr>
   <tr>
      <td>7.9 64位 ARM版</td>
   </tr>
   <tr>
      <td>Ubuntu</td>
      <td>20.04 64位 ARM版</td>
   </tr>
   <tr>
      <td>Debian</td>
      <td>11.2 64位 ARM版</td>
   </tr>
</table>


# soft
# 推荐软件版本
下表列出倚天云实例环境推荐软件版本

<table>
   <tr>
      <td>分类</td>
      <td>Software</td>
      <td>Version </td>
   </tr>
   <tr>
      <td rowspan="9">编译器及语言虚拟机</td>
      <td>GCC</td>
      <td>gcc 10.2.1</td>
   </tr>
   <tr>
      <td>LLVM</td>
      <td>LLVM13 / clang13</td>
   </tr>
   <tr>
      <td>GlibC</td>
      <td>glibc 2.32</td>
   </tr>
   <tr>
      <td>JDK</td>
      <td>JDK11</td>
   </tr>
   <tr>
      <td>JDK8</td>
      <td>8u292+</td>
   </tr>
   <tr>
      <td>Golang</td>
      <td>Go 1.18+</td>
   </tr>
   <tr>
      <td>Python</td>
      <td>Python 3.10+</td>
   </tr>
   <tr>
      <td>PHP</td>
      <td>7.4+</td>
   </tr>
   <tr>
      <td>ruby</td>
      <td>3.0+</td>
   </tr>
   <tr>
      <td>.NET</td>
      <td>5+</td>
   </tr>
   <tr>
      <td rowspan="3">Web</td>
      <td>Nginx</td>
      <td>1.20.1</td>
   </tr>
   <tr>
      <td>Apache（httpd）</td>
      <td>2.4.37</td>
   </tr>
   <tr>
      <td>NodeJS</td>
      <td>LTS 18+</td>
   </tr>
   <tr>
      <td rowspan="5">DB</td>
      <td>Mysql</td>
      <td>8.0.25</td>
   </tr>
   <tr>
      <td>Redis</td>
      <td>6.0.5</td>
   </tr>
   <tr>
      <td>mongodb</td>
      <td>4.2.15+</td>
   </tr>
   <tr>
      <td>HAProxy</td>
      <td>2.4+</td>
   </tr>
   <tr>
      <td>Flink</td>
      <td>1.11+</td>
   </tr>
   <tr>
      <td rowspan="3">Media</td>
      <td>x264</td>
      <td>0.164.x</td>
   </tr>
   <tr>
      <td>x265</td>
      <td>3.5</td>
   </tr>
   <tr>
      <td>ffmpeg</td>
      <td>4.3.2+</td>
   </tr>
   <tr>
      <td rowspan="4">ACC lib</td>
      <td>zlib</td>
      <td>1.2.11</td>
   </tr>
   <tr>
      <td>zstd</td>
      <td>1.5.2</td>
   </tr>
   <tr>
      <td>gzip</td>
      <td>1.2.11</td>
   </tr>
   <tr>
      <td>lz4</td>
      <td>1.9.3</td>
   </tr>
</table>

# 资源下载
[阿里巴巴开源镜像站](https://developer.aliyun.com/packageSearch?word=)

[dockerhub](https://hub.docker.com/search)


