## 简介
Java是解释型语言，理论上纯java应用可以跨架构运行。但实际上由于java应用经常通过JNI调用C编译的本地库，这会来带兼容性问题。Java语言应用迁移主要是解决JNI调用本地库的问题。需要注意的是解决本地库问题需要从两方面入手，一是您的应用依赖的的java包，如果当前使用的包不兼容ARM平台需要进行升级；二是您的应用本身开发的本地库，这部分需要重新编译java工程来解决。
## 迁移第一步: 选择JDK
ARM属于服务器端的新兴架构，因此选择JDK非常重要，合适的JDK可以大大减少遇到问题的概率同时也能获得更好的性能。
这里推荐使用Alibaba Dragonwell，Alibaba Dragonwell是阿里巴巴内部JDK的开源版本，针对倚天平台上各种业务形态做了大量优化。大家可以通过[https://dragonwell-jdk.io/](https://dragonwell-jdk.io/) 下载或者了解更多Alibaba Dragonwell的信息。
另外大家也可以通过[https://adoptium.net/zh-CN/temurin/releases](https://adoptium.net/zh-CN/temurin/releases) 下载JDK。
## 迁移第二步: 升级必要的依赖包
部分java三方包存在不兼容ARM的问题，如果您的应用运行中出现类似于以下的异常，就是使用了X86架构的本地库从而导致在ARM平台出现兼容性问题。
> Exception in thread "main" java.lang.UnsatisfiedLinkError: xxx.so: xxx.so: cannot open shared object file: No such file or directory (Possible cause: can't load AMD 64-bit .so on a AARCH64-bit platform)

通常情况下可以通过升级三方包版本解决。下表列出部分比较常见的三方包可能存在兼容性问题的三方包，推荐大家升级到推荐版本。

| 依赖包名称 | 推荐版本 |
| --- | --- |
| lz4-java | 1.4.0 |
| jna | 5.2.2 |
| snappy-java | 1.1.3 |
| icu4j | 68.1 |
| sqlite-jdbc | 3.20.0 |
| forest-sqlite-jdbc | 3.32.3.3 |
| netty-tcnative | 2.0.31 |
| netty-transport-native-epoll | 4.1.50 |

不过上表并不能覆盖所有不兼容ARM的三方包，为了全面排查ARM兼容性您需要检查所有引用的三方包。一个相对简单的办法是判断存在X86架构的so文件的三方包是否同时存在ARM架构的so文件，如果不存在则大概率这个三方包不支持ARM。
这里给出一个扫描三方包so文件的参考脚本，您可以把它放到您编译好的应用的目录中并执行脚本进行扫描。请注意不要在生产环境使用此脚本以免引起问题。
> rm -rf tmp
>
> mkdir tmp
>
> for jar in `find . -name *.jar`
>
> do
>
> if [ -f $jar ]
>
> then
>
> echo $jar
>
> cp -r $jar tmp/
>
> fi
>
> done
> 
> cd tmp
>
> for test in `ls`
>
> do
>
> name=`echo $test | sed "s/.jar//g"`
>
> echo $name
>
> mkdir $name
>
> cp -r $test $name
>
> cd $name
>
> unzip -o $test
>
> cd ..
>
> done
> 
> echo "========= starting Analysis =========="
>
> find . -name "*.so" -exec file {} \;
>

在最后会输出类似于如下的信息，我们可以看到lz4-1.3.0中有三个so文件，但均为x86架构，因此并不支持ARM架构。可以升级到1.4.0修复此问题，不过请注意1.4.0起已经更名为lz4-java
> ========= starting Analysis ==========
> ./lz4-1.3.0/win32/amd64/liblz4-java.so: PE32+ executable (DLL) (console) x86-64, for MS Windows
> ./lz4-1.3.0/linux/amd64/liblz4-java.so: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, BuildID[sha1]=2eafd0d4e86904e188b47565639318325108fffa, not stripped
> ./lz4-1.3.0/linux/i386/liblz4-java.so: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, BuildID[sha1]=41041674439aea5d1fd6c62b6d88f63da7600c9f, not stripped


## 迁移第三步: 重新构建java工程
Java工程常用的构建工具如maven等均为架构无关，因此这方面无需更改。仅需设置好JDK及gcc即可重新构建。JDK选择请参考第一步，GCC等请参考[C++迁移](C++.md)


## 优化建议
### JDK升级
为了在倚天上获得更好的性能及稳定性，如果您使用JDK8，请升级到JDK11或17。原因如下：
- Java8/11/17 以及未来的21是Long-term support(LTS)，维护时间长，其余为non-LTS，维护期短。Long-term support(LTS) 是Oracle管理Java版本生命周期的一个标准术语，Oracle原定每三年会指定一个LTS的Java版本，现在改成每两年。具体请参阅 https://www.oracle.com/java/technologies/java-se-support-roadmap.html
- ARM架构支持在Java9才被OpenJDK社区接受进入主干，因此以JDK9为分水岭，之后的JDK11/17对ARM支持较好，而JDK8尽管近两年页开始支持ARM，但相对11/17仍有所欠缺。阿里内部场景显示，从JDK8升级到JDK11有5%-20%不等的性能提升。
- 阿里巴巴内部场景显示社区JDK8对弱内存模型支持存在一定问题，JDK11可以解决。此外Albiaba Dragonwell8也解决了弱内存模型相关问题
- 如果只能使用JDK8，请务必升级到8u292及以上版本。因为从292版本OpenJDK8社区主干才支持ARM架构，早于292的JDK8在ARM架构服务器可能存在不可预知的问题

JDK11相对JDK8改动较大，存在一定的升级工作量。为了解决这个问题阿里云提供了专项升级工具EMT4J(Eclipse Migration Toolkit for Java)，可以大大加速不同JDK长期支持版本(8/11/17)的升级过程，帮助大家平滑迁移。EMT4J已经开源，大家可以访问[EMT4J官网](https://github.com/adoptium/emt4j) 试用

### 参数调优
- -XX:-UseBarriersForVolatile 此参数关闭UseBarriersForVolatile选项，适用于JDK11/8，JDK17无需设置。UseBarriersForVolatile控制如何实现volatile变量，关闭后会使用带同步语义的内存问指令操作volatile，开启后会使用普通内存访问指令再加上内存屏障指令访问volatile，后者相对低效。虽然这个参数是默认关闭的，但是在某些OS设置下会自动打开影响性能，，因此建议添加参数手动关闭这个选项。
- -XX:-TieredCompilation，此参数关闭分层编译。关闭分层编译可以减少JVM动态生成代码数目，提高icache/iTLB命中率。此优化适用于场景较为固定，流量较为稳定的应用使用。对于可能频繁执行新代码或是流量经常发生突变的应用可能出现编译开销过大的情况，不推荐设置。
- -XX:ReservedCodeCacheSize=240m 仅推荐JDK8使用。此参数用来调整CodeCache大小，由于JDK8中ARM默认的CodeCache为128M，少于X86架构的240M，因此在使用默认参数的话ARM平台一些情况下可能会由于CodeCache使用率过高导致一些性能问题。此参数将默认的CodeCacheSize设置成240M，与X86架构一致。特别注意如果当前Java运行参数已经设置过ReservedCodeCacheSize则不要再次设置。
