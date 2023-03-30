from PIL import Image
import numpy as np
import torch
from torchvision.models.detection.ssd import ssd300_vgg16, SSD300_VGG16_Weights
import time
import platform
import argparse


def profiling(model, x):
    from torch.profiler import profile, record_function, ProfilerActivity
    model.eval()
    with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
        pred = model(x)
    print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15, top_level_events_only=True))    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiling", action="store_true", required=False, help="model profiling")
    parser.add_argument("--bf16", action="store_true", required=False, help="bfloat16 mode")
    parser.add_argument("--batch", type=int, default=8, help="batch_size")
    args = parser.parse_args()

    if args.bf16 is True:
        torch.set_float32_matmul_precision("medium")

    model = ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT).to(torch.float32)

    x = [torch.rand(3, 300, 300).to(torch.float32) for _ in range(args.batch)]

    if args.profiling:
        profiling(model, x)
    else:
        print("Normal:")
        best_time = 1000
        model.eval()
        with torch.no_grad():
            for i in range(4):
                s = time.time()
                pred = model(x)
                e = time.time()
                if best_time > e - s:
                    best_time = e - s
                print(f"inference: {e-s} s")
        print(f"TARGET ssd Time {best_time:.4f}")
