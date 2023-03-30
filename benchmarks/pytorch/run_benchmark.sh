# We assume this benchmark running on different platforms:
#   IceLake, x86_64
#   Yitian 710, arm64
# Also, YiTian has bf16 support, while IceLake not.

# On ARM, PyTorch have two computation backend, Arm Compute Library(ACL) and OpenBLAS.
# They use bf16 to accelerate in different ways:
#   ACL uses environment variable DNNL_DEFAULT_FPMATH_MODE=BF16 to open acceleration
#   OpenBLAS use python code `torch.set_float32_matmul_precision("medium")` 

type=$1

if [ "$type" = "normal" ]; then

    cd resnet50
    python3 performance.py 2>&1 | grep "TARGET"

    cd ../ssd
    python3 performance.py 2>&1 | grep "TARGET"

    cd ../maskrcnn
    python3 performance.py 2>&1 | grep "TARGET"

    cd ../bert
    python3 performance.py 2>&1 | grep "TARGET"

elif [ "$type" = "blas" ]; then

    cd resnet50
    python3 performance.py --bf16 2>&1 | grep "TARGET"

    cd ../ssd
    python3 performance.py --bf16 2>&1 | grep "TARGET"

    cd ../maskrcnn
    python3 performance.py --bf16 2>&1 | grep "TARGET"

    cd ../bert
    python3 performance.py --bf16 2>&1 | grep "TARGET"

elif [ "$type" = "acl" ]; then

    cd resnet50
    DNNL_DEFAULT_FPMATH_MODE=BF16 python3 performance.py 2>&1 | grep "TARGET"

    cd ../ssd
    DNNL_DEFAULT_FPMATH_MODE=BF16 python3 performance.py 2>&1 | grep "TARGET"

    cd ../maskrcnn
    DNNL_DEFAULT_FPMATH_MODE=BF16 python3 performance.py 2>&1 | grep "TARGET"

    cd ../bert
    DNNL_DEFAULT_FPMATH_MODE=BF16 python3 performance.py 2>&1 | grep "TARGET"

else
    echo "Invalid param args: $type"
fi


