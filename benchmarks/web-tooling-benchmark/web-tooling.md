## 关于Web Tooling Benchmark
Web Tooling Benchmark is a benchmark suite designed to measure the JavaScript-related workloads commonly used by web developers, such as the core workloads in popular tools like [Babel](https://github.com/babel/babel) or [TypeScript](https://github.com/Microsoft/TypeScript). The goal is to measure **only** the JavaScript performance aspect (which is affected by the JavaScript engine) and not measure I/O or other unrelated aspects.

具体请访问[https://github.com/v8/web-tooling-benchmark](https://github.com/v8/web-tooling-benchmark)

## 测试环境
node: 18.2.0

v8: 10.1.124.8-node.13

## 运行方法
> docker run cape2/web-tooling-benchmark

## 结果解析
此测试的输出类似于
> sp 10.61

> mp 6.93719

sp为单线程测试结果，mp为多线程测试结果。数字为分数，越高越好
