# Run

```shell
# onednn + bf16
ONEDNN_DEFAULT_FPMATH_MODE=BF16 python resnet_tf1.py

# eigen
TF_ENABLE_ONEDNN_OPTS=0 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python resnet_tf1.py
```