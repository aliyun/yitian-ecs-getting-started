Python是一种解释型通用编程语言，得益于其友好的语法以及丰富的框架，常被用于编写运维工具，web服务、数据分析和深度学习程序。

# 1. 安装CPython解释器

## 1.1 使用操作系统包管理器安装

**centos:**

```bash
$sudo yum install python3 -y

$python3 --version   # centos 7.9
Python 3.6.8
```
Python3.6已经到达EOL，不再推荐使用。推荐使用Docker镜像。


**ubuntu:**

```bash
$sudo apt install python3 -y

$python3 --version   # ubuntu 20.04
Python 3.8.10

$python3 --version   # ubuntu 22.04
Python 3.10.4
```


## 1.2 使用docker镜像

首先不推荐直接使用`python:latest`镜像，该镜像包含了完整的pip和gcc构建环境，体积高达921M。且基于debian构建，并不是大家熟悉的centos和ubuntu。

### 对于不需要依赖复杂native库的应用推荐直接基于`python:alpine`镜像

举例：

```dockerfile
FROM python:alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories # 替换为中科大源
RUN apk add python3 py3-numpy
```
要注意以上使用`apk` OS包管理器安装来安装`numpy`，而没有使用`pip`。原因是**PyPI**提供的提前构建好的包依赖**glibc**，并不是适用于基于musl的alpine系统。

因此在alpine下使用pip安装`numpy`这一类依赖native实现的库时会尝试从头编译：
```
Collecting numpy
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/13/b1/0c22aa7ca1deda4915cdec9562f839546bb252eecf6ad596eaec0592bd35/numpy-1.23.1.tar.gz (10.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.7/10.7 MB 3.8 MB/s eta 0:00:00

RuntimeError: Broken toolchain: cannot link a simple C program.
```


### 没有特殊情况推荐基于熟悉的发行版构建

```dockerfile
FROM ubuntu

RUN apt update && apt install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
```

要注意这种情况下操作系统的包管理器决定了python的版本。


## 1.3 ~~通过源码编译CPython解释器~~

不建议直接通过源码编译CPython解释器，自行编译容易缺少ssl等模块的支持，且没有明显的收益。

## 1.4 推荐版本

- 推荐尽量使用最新版本的Python解释器，Python在**3.10**以及**3.11**版本通过faster-cpython项目获得了显著的性能提升。
- **Python 2.7** 在2020年到达 EOL，强烈建议不要继续使用Python 2。
- **Python 3.6** 已经在2021年底到达EOL，推荐至少使用Python3.7版本


# 2. 科学计算库(scipy, numpy)

Python 具有良好的扩展性，依靠第三方库实现高性能计算。
在科学计算领域，NumPy 和 SciPy 是目前被最广泛使用的 Python 库，而这两个库本身是调用更底层的 C/C++ 线性代数库（例如 MKL，OpenBLAS，BLIS 等）实现高性能计算的。
目前 OpenBLAS 包含针对倚天处理器优化的代码，因此我们推荐使用以 OpenBLAS 为后端构建的 NumPy 和 SciPy 库。

## 2.1 使用包管理器安装

可以直接使用各类包管理器直接安装 NumPy 或 SciPy。

使用 conda 或 pip 安装 NumPy 和 SciPy，例如 `pip3 install numpy scipy`，在 arm 平台，计算后端默认使用 OpenBLAS 库。

在 Ubuntu 或 Debian 上安装 NumPy 和 SciPy：
```bash
sudo apt install libopenblas-dev python3-numpy python3-scipy
```

## 2.2 从源码构建

环境依赖(以下编译器二选一)：

- [gcc 11](https://gcc.gnu.org/gcc-11/changes.html) 
- [clang 12](https://releases.llvm.org/12.0.0/tools/clang/docs/ReleaseNotes.html)

否则需要指定 `TARGET` 为 `ARMv8`，从而构建通用版本。

```bash
# 构建 OpenBLAS
git clone https://github.com/xianyi/OpenBLAS $HOME/OpenBLAS
cd $HOME/OpenBLAS
TARGET=NEOVERSEN2 BUILD_BFLOAT16=1 FC=gfortran USE_OPENMP=1 make -j8
sudo make install

# 构建 NumPy
git clone https://github.com/numpy/numpy $HOME/numpy
cd $HOME/numpy
pip install .

# 构建 SciPy
git clone https://github.com/scipy/scipy/ $HOME/scipy
cd $HOME/scipy
pip install .

```

测试是否安装成功，并查看是否使用 OpenBLAS 后端：
```bash
python -c "import numpy as np; np.show_config()"
python -c "import sicpy as sp; sp.show_config()"
```

## 2.3 实践案例

目前我们提供了 [NumPy](http://gitlab.alibaba-inc.com/ajdk/cape2/tree/master/benchmarks/numpy) 的 workload 和[测试镜像](https://hub.docker.com/r/cape2/numpy)。

直接运行我们提供的镜像可以获得 GEMM 和 SVD 计算的测试结果：

```bash
docker run --rm cape2/numpy:latest
```

或者进入 [grafana](http://dashboard.jvm.alibaba.net/d/6f3cgDj7z/cape2?orgId=1) 页面查看我们提供的可视化结果。


# 3. 深度学习库 

## 3.1 使用 Docker 镜像

**armswdev** 是arm提供的软件解决方案仓库，提供了在arm平台上的软件适配以及高性能实现。

**使用 Tensorflow 镜像**

```bash
# 开启 OneDNN+ACL 优化的 tensorflow 镜像
docker pull armswdev/tensorflow-arm-neoverse

# 启动镜像，假设项目代码在 home 目录中，挂载到容器的 /hostfs 目录下
docker run -it --rm -v $HOME:/hostfs armswdev/tensorflow-arm-neoverse

# 在容器中运行代码
cd /hostfs
python your_code.py
```

**使用 PyTorch 镜像**

使用方式与 Tensorflow 同理：
```bash
docker pull armswdev/pytorch-arm-neoverse
docker run -d -v $HOME:/hostfs -it armswdev/pytorch-arm-neoverse
```

## 3.2 使用 pip 安装

最新版本的 Tensorflow(2.10.0) 和 PyTorch(1.13.0) 可以使用 pip 包管理器安装，已经包含 OneDNN 和 ACL 的支持。
```bash
pip install tensorflow==2.10.0
pip install pytorch==1.13.0
```

## 3.3 实践案例

Tensorflow 模型推理优化：
1. 使用 OneDNN + ACL 后端的 tensorflow，获得针对倚天平台的优化
2. 避免在推理中使用 eager 模式
3. 模型参数冻结
4. 开启 BF16 优化

以测试图像分类任务 resnet50 模型的推理性能为例：
```python
from tensorflow.keras.applications.resnet import ResNet50

model = ResNet50()
# 使用 graph 模式而非 eager 模式
full_model = tf.function(lambda x: model(x))

# 模型参数冻结
full_model = full_model.get_concrete_function([tf.TensorSpec(model_input.shape, model_input.dtype) for model_input in model.inputs])
frozen_func = convert_variables_to_constants_v2(full_model)
frozen_func.graph.as_graph_def()

# 启动 session，完成推理，记录时间
session = tf.compat.v1.Session(graph=frozen_func.graph)
s = time.time()
predictions = session.run(["Identity:0"], feed_dict={"x:0": processed_image})
e = time.time()
print(f"inference: {e-s} s")
```

运行代码时开启 BF16 优化，能显著提升推理性能，但会降低参数精度：
```bash
TF_ENABLE_ONEDNN_OPTS=1 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python your_code.py
```

