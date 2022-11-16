## 关于 OpenBLAS
OpenBLAS 是一个开源的矩阵计算库，包含了诸多的精度和形式的矩阵计算算法。
OpenBLAS 被广泛应用于科学计算、数据分析、深度学习算法、人工智能等领域，被 PyTorch、NumPy、Julia、MXNet 等知名项目集成。
这个 Benchmark 主要评估 OpenBLAS 库在阿里云 ARM 平台上的性能，主要涉及科学计算和 AI 领域最常用的矩阵乘法任务。

## 测试环境
OpenBLAS: 0.3.21

编译工具: gcc 11

## 运行方法
```bash
docker run cape2/openblas
```

## 结果解析
此测试的输出类似于
```bash
1024 490.07
2048 65.94
```
开头的数字描述矩阵大小，例如 1024 表示矩阵的尺寸为 m = n = k = 1024。
后面的数字表示每秒可以完成矩阵乘法的次数，越高越好。


