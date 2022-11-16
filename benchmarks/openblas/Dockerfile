FROM ubuntu:22.04 AS compile-image

RUN sed -i -E 's/(security|archive|ports).ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt install --no-install-recommends -y build-essential git ca-certificates

WORKDIR /tmp
RUN git clone -b new_sbgemm https://github.com/imzhuhl/OpenBLAS.git --depth=1
WORKDIR OpenBLAS
RUN DYNAMIC_ARCH=1 BUILD_BFLOAT16=1 USE_THREAD=1 make -j16 && make install

WORKDIR /tmp
COPY benchmark.cpp Makefile ./
RUN make

FROM ubuntu:22.04 AS runtime-image
WORKDIR /tmp
COPY --from=compile-image /tmp/benchmark ./

ENTRYPOINT ./benchmark

