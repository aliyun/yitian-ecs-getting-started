# 关于 Eclipse Migration Toolkit for Java（EMT4J）

Eclipse Migration Toolkit for Java 是阿里巴巴向 Eclipse 社区贡献的开源项目，致力于为 Java 版本迁移提供高效的工具级解决方案。

* [Github](https://github.com/adoptium/emt4j)

# 功能介绍

帮助开发者发现应用中存在的兼容性问题，支持静态分析和运行时分析两种方式，报告的输出格式支持 text，json 以及 html。

# 快速开始

## 构建

### 环境要求

构建前需要在 `Maven` 的 `toolchains.xml` 配置 JDK 8 和 JDK 11，如

```xml
<?xml version="1.0" encoding="UTF-8"?>
<toolchains>
    <!-- JDK toolchains -->
    <toolchain>
        <type>jdk</type>
        <provides>
            <version>8</version>
            <vendor>openjdk</vendor>
        </provides>
        <configuration>
            <jdkHome>/Library/Java/JavaVirtualMachines/jdk1.8.0_281.jdk/Contents/Home</jdkHome>
        </configuration>
    </toolchain>
    <toolchain>
        <type>jdk</type>
        <provides>
            <version>11</version>
            <vendor>openjdk</vendor>
        </provides>
        <configuration>
            <jdkHome>/Library/Java/JavaVirtualMachines/jdk-11.0.9.jdk/Contents/Home</jdkHome>
        </configuration>
    </toolchain>
</toolchains>
```

构建命令：
```shell
$ mvn clean package -Prelease
```

## 使用

### 以 Agent（运行时分析）方式运行 EMT4J

以从 Java 8 迁移到 Java 11 为例：
```shell
$ java -javaagent:<path to agent>=file=output.dat,to=11 <Your Application>

# 生成以 HTML 格式的报告

$ bin/analysis.sh -o report.html output.dat
```

### 静态扫描

```shell
$ sh bin/analysis.sh -f 8 -t 11 -o report.html <jar direcorty or classes>...
```

### Maven 插件方式

在 pom.xml 增加一下配置：
```xml
    <plugin>
        <groupId>org.eclipse.emt4j</groupId>
        <artifactId>emt4j-maven-plugin</artifactId>
        <version>0.1</version>
        <executions>
            <execution>
                <phase>process-classes</phase>
                <goals>
                    <goal>check</goal>
                </goals>
            </execution>
        </executions>
        <configuration>
            <fromVersion>8</fromVersion>
            <toVersion>11</toVersion>
            <targetJdkHome>/Library/Java/JavaVirtualMachines/jdk-11.0.9.jdk/Contents/Home</targetJdkHome>
        </configuration>
    </plugin>
```

更多说明请参考[官方说明](https://github.com/adoptium/emt4j)。