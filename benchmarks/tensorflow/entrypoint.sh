cd resnet
(TF_ENABLE_ONEDNN_OPTS=1 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python3 resnet.py 2>&1 \
&& TF_ENABLE_ONEDNN_OPTS=0 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python3 resnet.py 2>&1) \
| grep KPI: | sort -k 3 -n -r | awk 'NR==1{print $2, $3}'

cd ../ssd
(TF_ENABLE_ONEDNN_OPTS=1 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python3 ssd_tf1.py 2>&1 \
&& TF_ENABLE_ONEDNN_OPTS=0 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python3 ssd_tf1.py 2>&1) \
| grep KPI: | sort -k 3 -n -r | awk 'NR==1{print $2, $3}'

cd ../bert
(TF_ENABLE_ONEDNN_OPTS=1 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python3 infer_tf.py 2>&1 \
&& TF_ENABLE_ONEDNN_OPTS=0 ONEDNN_DEFAULT_FPMATH_MODE=BF16 python3 infer_tf.py 2>&1) \
| grep KPI: | sort -k 3 -n -r | awk 'NR==1{print $2, $3}'
