import numpy as np
import time

def bench_gemm(m, n, k, iters):
    a = np.arange(float(m * n), dtype='float32').reshape(m, n)
    b = np.arange(float(n * k), dtype='float32').reshape(n, k)
    t0 = time.time()
    for i in range(iters): np.dot(a, b)
    print('gemm%d %f' % (n, iters / (time.time() - t0)))

bench_gemm(100, 200, 400, 10000)
bench_gemm(150, 300, 600, 1000)
bench_gemm(200, 400, 800, 1000)

a = np.arange(150 * 400).reshape(150, 400)
t0 = time.time()
for i in range(500): P, D, Q = np.linalg.svd(a, full_matrices=False)
print('svd ' + str(500 / (time.time() - t0)))
