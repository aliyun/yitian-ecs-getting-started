OPENBLAS_INCLUDE=/opt/OpenBLAS/include
OPENBLAS_LIB=/opt/OpenBLAS/lib

# COMPILE_OPTIONS=-I$(OPENBLAS_INCLUDE) -L$(OPENBLAS_LIB) -Wl,-rpath,$(OPENBLAS_LIB) -lopenblas
COMPILE_OPTIONS += -I$(OPENBLAS_INCLUDE) -L$(OPENBLAS_LIB) -static -lopenblas -lpthread

all: benchmark.cpp
	g++ -O2 benchmark.cpp $(COMPILE_OPTIONS) -o benchmark
