# PyTorch Benchmark

[倚天项目] 该项目包含 PyTorch benchmark 和 PyTorch 镜像的构建文件。

PyTorch 在 ARM 设备上有两个可选的计算后端：OpenBLAS 或者 Arm Compute Library(ACL)。
当前在不同的 benchmark 上，两者的性能表现互有高低，因此同时提供两个计算后端的 PyTorch 供用户选择。

## 测试性能

```bash
# 拉取 modelzoo 镜像，进行推理测试
docker pull accc-registry.cn-hangzhou.cr.aliyuncs.com/pytorch/pytorch:modelzoo
docker run --rm accc-registry.cn-hangzhou.cr.aliyuncs.com/pytorch/pytorch:modelzoo
```

## Workload
四个测试
- ResNet50
- SSD
- Mask R-CNN
- BERT

各个目录下包含 `performance.py` 文件，运行该文件，得到单个测试的性能结果：
```bash
python3 performance.py

# PyTorch + OpenBLAS 开启 bf16
python3 performance.py --bf16

# PyTorch + ACL 开启 bf16
DNNL_DEFAULT_FPMATH_MODE=BF16 python3 performance.py --bf16

# 显示各个算子耗时
python3 performance.py --profiling
```

输出格式
```bash
# 输出 workload 的推理时间，单位秒
[TARGET] <workload> Time <inference time>
```

## BF16 预测结果校验
各个目录下包含 `validate.py` 文件，运行该文件，命令如下：
```bash
python3 validate.py
# PyTorch + OpenBLAS 开启 bf16
python3 validate.py --bf16
# PyTorch + ACL 开启 bf16
DNNL_DEFAULT_FPMATH_MODE=BF16 python3 performance.py --bf16
```
执行后会自动下载预训练模型，预测结果，该步骤主要验证开启 bf16 是否会影响预测结果。

验证结果说明：
- ResNet50: 显示最高的五个类别的概率
- SSD: 输出预测图像，保存在同级目录下
- Mask R-CNN: 输出预测图像，保存在同级目录下
- BERT: Q&A模型，输出回答


## 镜像构建

构建 PyTorch 镜像的 Dockerfile 在 `pytorch_env` 中：
- Dockerfile.torch_acl 用于构建 PyTorch + ACL
- Dockerfile.torch_blas 用于构建 PyTorch + OpenBLAS

构建指令
```bash
# 例子
docker buildx build --platform linux/arm64 -f Dockerfile.torch_acl accc-registry.cn-hangzhou.cr.aliyuncs.com/pytorch/pytorch:torch1.13.0_acl --load .
```

构建 PyTorch modelzoo 镜像的 Dockerfile 在当前目录，modelzoo 镜像包含多个 benchmark 用于性能测试。

## 镜像 Tag

当前镜像Tag
- `torch1.13.0_acl`: PyTorch 1.13.0 with Arm Compute Library
- `torch1.13.0_openblas`: PyTorch 1.13.0 with OpenBLAS
- `torch1.13.0_acl_modelzoo`: `torch1.13.0_acl` + benchmarks
- `torch1.13.0_openblas_modelzoo`: `torch1.13.0_openblas` + benchmarks
- `torch1.13.0_x86_modelzoo`: PyTorch 1.13.0 x86 version + benchmarks
- `modelzoo`: (latest for both x86 and arm) `torch1.13.0_acl_modelzoo` and `torch1.13.0_x86_modelzoo`
