from PIL import Image
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision.models import resnet50, ResNet50_Weights
import time
import platform
import glob
import argparse


class SimpleDataset(Dataset):
    def __init__(self, mean, std, datatype) -> None:
        super(SimpleDataset, self).__init__()
        data_path = "./data"
        imgs_path = glob.glob(f"{data_path}/*.JPEG")
        imgs_path.sort()
        self.imgs_path = imgs_path
        self.mean = mean
        self.std = std
        self.datatype = datatype

    def __getitem__(self, index):
        img = Image.open(self.imgs_path[index]).convert("RGB")
        img = img.resize((224, 224))
        img = np.asarray(img).astype("float32")
        img = np.transpose(img, (2, 0, 1))  # CHW
        img = (img / 255 - self.mean) / self.std
        img = torch.from_numpy(img).to(self.datatype)

        return {
            'img': img,
            'label': "none"
        }

    def __len__(self):
        return len(self.imgs_path)
        # return 512


def load_image():
    img = Image.open("data/ILSVRC2012_val_00000001.JPEG").convert("RGB")
    resized_img = img.resize((224, 224))
    img_data = np.asarray(resized_img).astype("float32")
    img_data = np.transpose(img_data, (2, 0, 1))  # CHW

    # Normalize according to the ImageNet input specification
    imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
    imagenet_stddev = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
    norm_img_data = (img_data / 255 - imagenet_mean) / imagenet_stddev

    # Add the batch dimension, as we are expecting 4-dimensional input: NCHW
    img_data = np.expand_dims(norm_img_data, axis=0).repeat(32, axis=0)

    return img_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-bf16", action="store_true", required=False, help="old version")
    parser.add_argument("--bf16", action="store_true", required=False, help="bfloat16 support")
    args = parser.parse_args()

    if args.old_bf16 is True:
        torch_type = torch.bfloat16
    else:
        torch_type = torch.float32
        if args.bf16 is True:
            torch.set_float32_matmul_precision("medium")

    imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
    imagenet_stddev = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
    infer_dataset = SimpleDataset(imagenet_mean, imagenet_stddev, torch_type)
    infer_loader = DataLoader(infer_dataset, batch_size=1, shuffle=False)

    # img_data = load_image()

    model = resnet50(weights=ResNet50_Weights.DEFAULT).to(torch_type)

    model.eval()
    for i, item in enumerate(infer_loader):
        with torch.no_grad():
        # with torch.autocast(device_type="cpu", dtype=torch.bfloat16):
            x = item["img"]
            # torch.set_float32_fast_math_mode("BF16")
            pred = model(x)
            # torch.set_float32_fast_math_mode("FP32")
            # pred2= model(x)
            # print(torch.sum(torch.abs(pred1-pred2) > 0.2))
            # print(torch.sum(torch.abs(pred1)))
            # pred1 = torch.nn.functional.softmax(pred1, dim=1)
            # raw_rst = torch.topk(pred, k=5, dim=1)
            # print(raw_rst)

            result = torch.nn.functional.softmax(pred, dim=1)
            result = torch.topk(result, k=5, dim=1)
            print(result)
