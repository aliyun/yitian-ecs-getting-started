import torch
import time
import json
import numpy as np
from PIL import Image
from torchvision.transforms import transforms
from torchvision.models.detection.mask_rcnn import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights
import argparse
import os


def profiling(model, x):
    from torch.profiler import profile, ProfilerActivity
    model.eval()
    with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
        pred = model(x)
    print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=15, top_level_events_only=True))


def inference(model, x):
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
    print(f"TARGET maskrcnn Time {best_time:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bf16", action="store_true", required=False, help="bfloat16 mode")
    parser.add_argument("--profiling", action="store_true", required=False, help="model profiling")
    parser.add_argument("--batch", type=int, default=8, help="batch_size")
    args = parser.parse_args()

    if args.bf16 is True:
        torch.set_float32_matmul_precision("medium")
    
    model = maskrcnn_resnet50_fpn(weights=MaskRCNN_ResNet50_FPN_Weights.DEFAULT)

    image = Image.open("./data/val2017/000000252219.jpg").convert('RGB')
    image = np.asarray(image).astype("float32")
    image = np.transpose(image, (2, 0, 1))  # CHW
    image = image / 255.0    

    image = np.expand_dims(image, axis=0).repeat(args.batch, axis=0)
    print(image.shape)
    x = torch.from_numpy(image).contiguous()

    if args.profiling:
        profiling(model, x)
    else:
        inference(model, x)
    
