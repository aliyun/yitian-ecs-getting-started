C/C++属于静态编译语言，C/C++编译则是将源代码经由编译器、汇编器处理生成机器指令，再通过链接器和库函数结合生成可执行程序。而X86和aarch64属于不同的架构，指令集也不同，其开发的程序从x86处理器迁移到AArch64上时，必须要重新编译。

## C/C++代码迁移
C/C++工程一般包含两类文件：C/C++源码(.h, .hpp, .c, .cpp, .cc...)，构建脚本(Makefile, CMakeLists.txt, .bazelrc...)。构建脚本中涉及的迁移内容主要是用于指定数据类型、处理器架构、代码生成等的编译选项；而C/C++源码中涉及的迁移内容则主要是平台架构&指令相关的宏，builtin函数，intrinsic函数以及内联汇编
- 构建脚本迁移
  - 指定代码生成为64bit， 从 `-m64` 换成 `-mabi=lp64`
  - 大多数 x86 编译器将 char 类型默认为有符号的，而在 aarch64 下通常 char 类型默认为无符号的，在迁移过程中，需要确保 char 被当作有符号类型处理，因此 aarch64 上要添加 `-fsigned-char`
  - 指定处理器架构的选项march mtune mcpu换成 `-march=armv8-a+sve2 -mcpu=neoverse-n1`
- 源码迁移
  - 宏相关  
    1) 指定平台架构相关的宏定义：如`__x86_64`和`__amd64`等X86相关宏需要换成`__aarch64__`  
    2) SIMD等特定平台指令相关宏定义：如`__SSE`和`__AVX`等需要换成NEON/SVE在对应的编译器中的自定义宏`__ARM_NEON`和`__ARM_FEATURE_SVE`等  
    3) 可以通过`gcc -march=armv8-a+sve2 -mcpu=neoverse-n1 -dM -E -<  /dev/null`来查看倚天服务器所支持的所有宏
  - builtin函数  
    1) 类似于builtin_ia32_xxx需要换成相同语义的builtin_aarch64_xxx，比如crc相关函数`__builtin_ia32_crc32qi(a, b)`需要换成aarch64 builtin的`__builtin_aarch64_crc32cb(a, b)``
  - intrinsic函数  
    1) 大部分的工作量集中在simd相关intrinsic的迁移，首先替换头文件为`arm_neon.h`，`arm_sve.h`  
    2) 其次参考`https://developer.arm.com/architectures/instruction-sets/simd-isas`替换intrinsic，这里需要将特定指令和数据类型都转换成倚天平台支持的。例如：x86的`__m128 _mm_load_ps`需要换成`float32x4 vld1q_f32`，  
    3) 由于x86支持avx指令，寄存器长度为256bit，倚天服务器目前只支持128bit长度寄存器，则需要相同语义的展开。比如：`__m256d _mm_add_ps` 则需要aarch64上两条simd指令 `vaddq_f32 vaddq_f32`。另外，倚天服务器虽然支持sve指令，但由于其编程模式的特殊性，不推荐直接使用sve intrinsic  
    4) 另外一种方式则是基于`https://github.com/DLTcollab/sse2neon`和`https://github.com/simd-everywhere/simde`等开源工程来尝试自动替换
  - 内联汇编
    1) 参考`https://gcc.gnu.org/onlinedocs/gcc/Using-Assembly-Language-with-C.html#Using-Assembly-Language-with-C`的规则将x86汇编指令替换成相同语义的aarch64指令。  
    2) 例如:` __asm__("bswap %0": "=r"(val): "0"(val))`则可以用相同语义的`rev`指令替换成`__asm__("rev %[dst], %[src]":  [dst]"=r"(val): [src]"r"(val))`

## 编译器及推荐参数
- 较新的编译器能够为倚天服务器提供更好的支持和优化。请使用操作系统上可用的最新编译器版本，或者我们推荐的GCC10&CLANG/LLVM13及以上版本
- ARM64体系结构相关优化参数

| 选项      | 取值    | 说明  |
| :---      | :---    | :---  |
| `-march=arch{+[no]feature}*`     | 指定ARM64平台的体系结构，arch指定具体的ARMV8体系结构及扩展。取值有"armv8-a","armv8.1-a","armv8.2-a","armv8.3-a","armv8.4-a","armv8.5-a" 或"native"; feature可以打开或关闭具体的体系结构特色功能     | feature取值可以是：`crc、crypto、fp、simd、sve、lse、rdma、fp16、fp16fml、rcpc、dotprod、aes、sha2、sha3、sm4、profile、rng、memtag、sb、ssbs、predres、sve`等。具体含义可以参考GCC官方文档：`https://gcc.gnu.org/onlinedocs/gcc-9.2.0/gcc/AArch64-Options.html#aarch64-feature-modifiers`   |
| `-mcpu=cpu{+[no]feature}*`  | 指定ARM64平台的处理器，cpu指定具体的处理器类型。feature与-march相同，可以打开或关闭具体的处理器特色功能       | 该选项指定编译器为特定机器类型生成优化代码，并针对特定机器进行流水线重排以达到最佳性能      |
| `-mtune=name`  | 该选项除不会生成指定处理器特色指令外，其他功能一致。如果同时指定-mcpu和-mtune，则-mtune优先级更高      | -mcpu与-mtune选择一 个使用即可，这里建议统一使用-mtune选项      |

- LSE使能
  - LSE（Large System Extensions）是ARMv8.1新增的原子操作指令集。在LSE之前，如果想实现某个原子操作，必须要使用带有load_acquire/store_release的指令，如LDXR和STXR,但这两个指令的操作本质上是很多CPU核去抢某个内存变量的独占访问，以前ARM主要用来在低功耗设备上运行，CPU核并不多，不会存在太大的问题。但在数据中心发展场景下，ARM处理器已经发展到几十上百核，如果还是独占访问会存在严重的性能问题。因此，为了支持这种大型系统，在ARMv8.1中特意加入了大量原生原子操作指令以优化性能。在有较多多线程竞争的场景下，使用LSE指令集会有比较明显的性能提升。

- 针对倚天服务器建议指定-march=armv8.6+crypto+sve2 -mtune=neoverse-n1

## 如何确定当前的编译参数

在生产环境中，编译参数的产生和使用可能较为复杂。要准确了解使用的编译参数有以下几种方案，可根据自身环境选择：

1. Compilation Database

    Compilation database 是一个 JSON 文件，它记录了软件项目中每个文件的编译细节，包括编译的具体参数。

    在不同的平台/工具链下，主要有如下几种方式可生成：

  1.1. `CMAKE_EXPORT_COMPILE_COMMANDS=ON` (CMake >= 3.5)

    在构建时设置 `CMAKE_EXPORT_COMPILE_COMMANDS` 变量为 `ON`。可以在 CMakeLists.txt 中添加 `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` 设置，或者在运行 CMake 时传递 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` 参数。CMake 会在构建目录中生成 `compile_commands.json` 文件。该方案不需要实际运行构建。

  1.2. [Bear](https://github.com/rizsotto/Bear) (Make / CMake / Ninja)

     使用方法：首先安装 Bear。构建项目时，使用 Bear 包装你的构建命令。例如，如果通常使用 `make`，则改为使用 `bear -- make`。Bear 将拦截编译命令并创建 compile_commands.json 文件。

  1.3. [Bazel Compile Commands Extractor](https://github.com/hedronvision/bazel-compile-commands-extractor)

     使用方法：按照提供的插件提供的指南安装工具。它会在 Bazel 运行构建时同步分析并生成相应的 compile_commands.json 文件。

2. 构建日志

   使用构建系统的详细日志可以获取编译过程中的每个命令，包括编译器的调用和传递的参数。

  2.1. `VERBOSE=1` (Make / CMake)
    
    使用方法：对于 Make：在执行 make 命令时，添加 `VERBOSE=1` 参数，例如 `make VERBOSE=1`。这会打印出更详细的构建过程信息。也可使用环境变量控制该行为，方便无法修改构建环境的场景：
    ```
    export VERBOSE=1
    make
    ```
    对于 CMake：在构建时设置 `CMAKE_VERBOSE_MAKEFILE` 变量为 `ON`。可以在 CMakeLists.txt 中添加 `set(CMAKE_VERBOSE_MAKEFILE ON)` 设置，或者在运行 CMake 时传递 `-DCMAKE_VERBOSE_MAKEFILE=ON` 参数。这同样会让构建过程输出详细信息。

### 使用案例

以 opencv 为例，说明以上各种方式的用法及输出。
1. 首先获取 opencv 源码，同时创建构建环境。

    ```
    git clone --depth=1 https://github.com/opencv/opencv.git
    mkdir build
    cd build
    ```

2. 使用 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` 生成编译数据库

    ```
    cmake ../opencv -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    # 在 cmake 配置完成后即可在当前目录下看到 `compile_commands.json`
    # 确认每个命令中都包含 `-fsigned-char` 参数
    jq '[.[] | .command | contains("-fsigned-char")] | all' compile_commands.json
    # 输出 true，说明 opencv 已正确添加了 `-fsigned-char` 参数。
    ```

3. 或使用 `bear` 生成编译数据库

    ```
    # AnolisOS / CentOS 上安装 bear
    yun install -y bear
    # Ubuntu 上安装 bear
    apt-get install -y bear
    cmake ../opencv
    bear -- make -j
    jq '[.[] | .command | contains("-fsigned-char")] | all' compile_commands.json
    ```

4. 或通过构建日志判断

    ```
    cmake ../opencv -DCMAKE_VERBOSE_MAKEFILE=ON
    make
    # 或
    cmake ../opencv
    make VERBOSE=1
    ```
    输出类似：
    ```
    ...
    [  0%] Building C object 3rdparty/libjpeg-turbo/src/simd/CMakeFiles/jsimd.dir/arm/jcgray-neon.c.o
    <具体的编译命令，由于过长省略>
    ...
    ```
    在编译日志里可以看到具体使用的参数。

通过以上几种方法，可以确定在实际的编译中是否使用了特定的参数，从而更好地指导迁移。
