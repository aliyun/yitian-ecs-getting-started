# 使用多架构容器镜像

多架构容器镜像支持在一个镜像内包含多种架构的镜像，可以简化在不同架构主机上的运行和维护成本。目前阿里云镜像服务 ACR 、容器服务 ACK 均已支持多架构镜像。

用户可以使用 [EasyYitian](../EasyYitian/README.md) 辅助构建多架构容器镜像，或自行基于阿里云提供的多架构优化镜像进行构建。

# 构建多架构容器镜像

下面的实例演示如何构建和推送一个 Java 应用的多架构镜像。

开源的 Dragonwell JDK 提供了 x64 和 arm64 的多架构镜像，并针对倚天架构进行了性能和稳定性的优化，推荐作为 Java 容器应用的基础镜像。

如下以空应用作为示例，展示基于 Dragonwell 的多架构 Java 应用构建方式。

```Dockerfile
# Dockerfile
FROM dragonwell-registry.cn-hangzhou.cr.aliyuncs.com/dragonwell/dragonwell:dragonwell-11.0.15.11.9_jdk-11.0.15-ga-ubuntu

CMD ["java", "-version"]
```

如原有的构建命令为：
```
docker build . -t registry.cn-hangzhou.aliyuncs.com/app/myapp:latest
```
如下命令可以构建并将产生的多架构镜像推送到镜像仓库：
```
docker buildx build --platform linux/amd64,linux/arm64/v8 . -t registry.cn-hangzhou.aliyuncs.com/app/myapp:latest --push
```
首次使用`docker buildx`时可能需要创建构建环境：
```
docker buildx create
```


随后，在不同架构的容器环境中拉取`registry.cn-hangzhou.aliyuncs.com/app/myapp:latest`镜像时，会自动匹配正确的架构，简化部署流程，也可以达到混合部署等目的。

# 语言迁移相关

在构建多架构容器镜像时首先需要确认应用本身没有架构相关的功能，这部分可以参考本文档的[语言迁移](../Languages/)部分。
