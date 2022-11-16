## 关于php bench

目前包含了 php 源码提供的 bench.php 和 micro_bench.php。

运行过程中会创建 `nproc` 个 php 进程。

## 测试环境

php 7.4 和 php 8.1。

## 运行方法

php 7.4

```
$ docker run cape2/php-7.4
```


php 8.1

```
$ docker run cape2/php-8.1
```

## 结果解析

输出格式如下：

```
micro_bench.php 0.295465
bench.php 1.74216
```

数值通过计算 `nproc` 除以运行总时间得到，越大表示性能越好。
