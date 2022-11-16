# 关于 Eclipse Jifa

Eclipse Jifa 是阿里巴巴向 Eclipse 社区贡献的开源项目，致力于提高在生产环境排查 Java 应用常见问题的效率。

* [Github](https://github.com/eclipse/jifa)

# 功能介绍

目前包含三大功能：
- Heap Dump 分析
  ![Sample](https://raw.githubusercontent.com/wiki/eclipse/jifa/resources/jifa-sample.jpg)
- GC 日志分析
  ![Sample](https://raw.githubusercontent.com/wiki/eclipse/jifa/resources/jifa-gc-log-analysis-sample.jpg)
- Thread Dump 分析

# 快速开始

## 构建

### 环境要求

构建前需要在 `Maven` 的 `toolchains.xml` 配置 JDK 8 和 JDK 11，如
构建前需要将 `JAVA_HOME` 指向 JDK 8

构建命令：
```shell
$ ./gradlew buildJifa
```

## Demo

``` shell
$ docker pull jifadocker/jifa-worker:demo
$ docker run -p 8102:8102 jifadocker/jifa-worker:demo
```

更多说明请参考[官方说明](https://github.com/eclipse/jifa)。