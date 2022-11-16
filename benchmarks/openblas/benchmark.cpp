/**
 * run sbgemm on YITIAN
 * run sgemm on other, becasue they doesn't support bf16 gemm
 */ 

#include <random>
#include <cstddef>
#include <string>
#include <fstream>
#include <chrono>
#include <iostream>
#include "cblas.h"

constexpr int REP_CNT = 50;

enum class InitVecFlag {
    Zero,
    One,
    IncreaseByOne,
    RandonValue,
};

void fill_vector(float *v, size_t length, InitVecFlag flag) {
    std::random_device rd;
    std::mt19937 mt(rd());
    std::uniform_real_distribution<float> dist(-1.0, 1.0);

    for (size_t i = 0; i < length; i++) {
        switch (flag)
        {
        case InitVecFlag::Zero : 
            v[i] = 0;
            break;
        case InitVecFlag::One : 
            v[i] = 1;
            break;
        case InitVecFlag::IncreaseByOne : 
            v[i] = i;
            break;
        case InitVecFlag::RandonValue :
            v[i] = dist(mt);
            break;
        default:
            printf("Error InitVecFlag value\n");
            exit(1);
        }
    }
}

void copy_vector(float *src, float *dst, size_t size) {
    for (size_t i = 0; i < size; i++) {
        dst[i] = src[i];
    }
}

void vec_fp32_to_bf16(float *src, bfloat16 *dst, size_t size) {
    for (size_t i = 0; i < size; i++) {
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
        dst[i] = *(reinterpret_cast<bfloat16 *>(&src[i]));
#else
        dst[i] = *(reinterpret_cast<bfloat16 *>(&src[i])+1);
#endif
    }
}

int run_sbgemm(int mat_size) {
    int M = mat_size;
    int K = mat_size;
    int N = mat_size;

    double gflops = 2.0 * M * N * K * 1.0e-09;

    float alpha = 1;
    float beta = 0;
    int lda = M; // col major order
    int ldb = K;
    int ldc = M;

    float *FA = new float[M * K];
    float *FB = new float[K * N];
    float *C = new float[M * N];
    float *myc = new float[M * N];


    fill_vector(FA, M * K, InitVecFlag::RandonValue);
    fill_vector(FB, K * N, InitVecFlag::RandonValue);
    fill_vector(C, M * N, InitVecFlag::Zero);

    bfloat16 *A = new bfloat16[M * K];
    bfloat16 *B = new bfloat16[K * N];
    vec_fp32_to_bf16(FA, A, M * K);
    vec_fp32_to_bf16(FB, B, K * N);

    /* Time of implementation */
    double dtime = 0.0;
    for (int rep = 0; rep < REP_CNT; rep++) {
        copy_vector(C, myc, M * N);
        auto start = std::chrono::steady_clock::now();
        cblas_sbgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, M, N, K,
            alpha, A, lda, B, ldb, beta, myc, ldc);
        auto end = std::chrono::steady_clock::now();
        std::chrono::duration<double, std::milli> elapsed = end - start;
        dtime += elapsed.count() * 1.0e-3;  // s
        // printf("%.2lf GFLOPS, %.2lf ms\n", gflops / (elapsed.count() * 1.0e-3), elapsed.count());
    }
    printf("%d %.2lf\n", mat_size, 1.0 * REP_CNT / dtime);

    delete[] FA;
    delete[] FB;
    delete[] A;
    delete[] B;
    delete[] C;
    delete[] myc;

    return 0;
}

int run_sgemm(int mat_size) {
    int M = mat_size;
    int K = mat_size;
    int N = mat_size;

    double gflops = 2.0 * M * N * K * 1.0e-09;

    float alpha = 1;
    float beta = 0;
    int lda = M; // col major order
    int ldb = K;
    int ldc = M;

    float *A = new float[M * K];
    float *B = new float[K * N];
    float *C = new float[M * N];
    float *myc = new float[M * N];

    fill_vector(A, M * K, InitVecFlag::RandonValue);
    fill_vector(B, K * N, InitVecFlag::RandonValue);
    fill_vector(C, M * N, InitVecFlag::Zero);

    /* Time of implementation */
    double dtime = 0.0;
    for (int rep = 0; rep < REP_CNT; rep++) {
        copy_vector(C, myc, M * N);
        auto start = std::chrono::steady_clock::now();
        cblas_sgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, M, N, K,
            alpha, A, lda, B, ldb, beta, myc, ldc);
        auto end = std::chrono::steady_clock::now();
        std::chrono::duration<double, std::milli> elapsed = end - start;
        dtime += elapsed.count() * 1.0e-3;  // s
        // printf("%.2lf GFLOPS, %.2lf ms\n", gflops / (elapsed.count() * 1.0e-3), elapsed.count());
    }
    printf("%d %.2lf\n", mat_size, 1.0 * REP_CNT / dtime);

    delete[] A;
    delete[] B;
    delete[] C;
    delete[] myc;

    return 0;
}

int main() {
    std::string tmp;

    std::ifstream fin("/sys/devices/system/cpu/cpu0/regs/identification/midr_el1");

    if (fin.fail()) {
        run_sgemm(1024);
        run_sgemm(2048);
        fin.close();
        return 0;
    }
    
    fin >> tmp;
    fin.close();

    /**
     * MIDR_EL1
     *
     * 31          24 23     20 19          16 15          4 3        0
     * -----------------------------------------------------------------
     * | Implementer | Variant | Architecture | Part Number | Revision |
     * -----------------------------------------------------------------
     */
    auto midr_el1 = std::stoul(tmp, nullptr, 0);
    int implementer = (midr_el1 >> 24) & 0xFF;
    int part        = (midr_el1 >> 4)  & 0xFFF;

    if (implementer == 0x41 && part == 0xd49) { // ARM && Neoverse N2
        run_sbgemm(1024);
        run_sbgemm(2048);
    } else {
        run_sgemm(1024);
        run_sgemm(2048);
    }
    return 0;
}
