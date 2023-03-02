from PIL import Image
import numpy as np
import torch
from torchvision.models import resnet50, ResNet50_Weights
import time
import platform
import argparse


def cpuinfo() -> str:
    arch = platform.processor()
    if arch == "aarch64":
        with open('/proc/cpuinfo', 'r') as f:
            info = f.readlines()
            for line in info:
                if "CPU part" in line and "0xd49" in line.split(":")[1]:
                    return "neoverse n2"
        return "arm64"
    else:
        return "amd64"


def load_image(args):
    img = Image.open("data/ILSVRC2012_val_00000001.JPEG").convert("RGB")
    resized_img = img.resize((224, 224))
    img_data = np.asarray(resized_img).astype("float32")
    img_data = np.transpose(img_data, (2, 0, 1))  # CHW

    # Normalize according to the ImageNet input specification
    imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
    imagenet_stddev = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
    norm_img_data = (img_data / 255 - imagenet_mean) / imagenet_stddev

    # Add the batch dimension, as we are expecting 4-dimensional input: NCHW
    img_data = np.expand_dims(norm_img_data, axis=0).repeat(args.batch, axis=0)

    return img_data


def profiling(model, x):
    from torch.profiler import profile, ProfilerActivity
    model.eval()
    with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
        pred = model(x)
    print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15, top_level_events_only=False))


def inference(model, x):
    print("Normal:")
    best_time = 1000
    model.eval()
    with torch.no_grad():
        for i in range(6):
            s = time.time()
            pred = model(x)
            e = time.time()
            if best_time > e - s:
                best_time = e - s
            print(f"inference: {e-s} s")
    print(f"TARGET resnet50 Time {best_time:.4f}")

    print("JIT:")
    traced_model = torch.jit.trace(model, x)
    traced_model = torch.jit.freeze(traced_model)
    traced_model = torch.jit.optimize_for_inference(traced_model)
    best_time = 1000
    for i in range(6):
        s = time.time()
        pred = traced_model(x)
        e = time.time()
        print(f"inference: {e-s} s")
        if best_time > e - s:
            best_time = e - s

    print(f"best inference time: {best_time:.4f}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-bf16", action="store_true", required=False, help="All bfloat16")
    parser.add_argument("--bf16", action="store_true", required=False, help="fast math mode")
    parser.add_argument("--batch", type=int, default=32, help="batch_size")
    parser.add_argument("--profiling", action="store_true", required=False, help="model profiling")
    args = parser.parse_args()

    img_data = load_image(args)

    if args.old_bf16 is True:
        torch_type = torch.bfloat16
    else:
        torch_type = torch.float32
        if args.bf16 is True:
            torch.set_float32_matmul_precision("medium")

    x = torch.from_numpy(img_data).to(torch_type)

    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2).to(torch_type)

    # print(torch.get_float32_matmul_precision())

    if args.profiling:
        profiling(model, x)
    else:
        inference(model, x)

    
