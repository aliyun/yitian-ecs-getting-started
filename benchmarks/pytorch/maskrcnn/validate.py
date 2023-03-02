import os
import torch
import time
import json
import numpy as np
from PIL import Image
from torchvision.transforms import transforms
from torchvision.models.detection.mask_rcnn import maskrcnn_resnet50_fpn, MaskRCNN, MaskRCNN_ResNet50_FPN_Weights
import random
import cv2
import argparse


def get_val_data():
    anno_file = "./data/annotations/instances_val2017.json"
    with open(anno_file) as f:
        anno_data = json.load(f)

    file_name = anno_data["images"][0]["file_name"]
    img_id = anno_data["images"][0]["id"]

    anno_list = []
    for item in anno_data["annotations"]:
        if item["image_id"] == img_id:
            anno_list.append(item)
    
    categories = anno_data["categories"]
    
    return file_name, anno_list, categories


def draw(image):
    # this will help us create a different color for each class
    COLORS = np.random.uniform(0, 255, size=(len(categories), 3))
    alpha = 1 
    beta = 0.6  # transparency for the segmentation map
    gamma = 0   # scalar added to each sum
    for i in range(len(masks)):
        red_map = np.zeros_like(masks[i]).astype(np.uint8)
        green_map = np.zeros_like(masks[i]).astype(np.uint8)
        blue_map = np.zeros_like(masks[i]).astype(np.uint8)

        # apply a randon color mask to each object
        color = COLORS[random.randrange(0, len(COLORS))]
        red_map[masks[i] == 1], green_map[masks[i] == 1], blue_map[masks[i] == 1] = color
        # combine all the masks into a single image
        segmentation_map = np.stack([red_map, green_map, blue_map], axis=2)
        #convert the original PIL image into NumPy format
        image = np.array(image)
        # convert from RGN to OpenCV BGR format
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # apply mask on the image
        cv2.addWeighted(image, alpha, segmentation_map, beta, gamma, image)
        # draw the bounding boxes around the objects
        cv2.rectangle(image, boxes[i][0], boxes[i][1], color=color, thickness=2)
        # put the label text above the objects
        cv2.putText(image , labels[i]['name'], (boxes[i][0][0], boxes[i][0][1]-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 
                    thickness=2, lineType=cv2.LINE_AA)
    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bf16", action="store_true", required=False, help="bfloat16 mode")
    args = parser.parse_args()

    if args.bf16 is True:
        torch.set_float32_matmul_precision("medium")

    file_name, anno_list, categories = get_val_data()

    orig_image = Image.open(os.path.join("./data/val2017", file_name)).convert('RGB')
    image = orig_image.copy()
    trans = transforms.Compose([
        transforms.ToTensor(),
    ])
    image = trans(image)
    image = image.unsqueeze(0)

    model = maskrcnn_resnet50_fpn(weights=MaskRCNN_ResNet50_FPN_Weights.DEFAULT)

    model.eval()
    with torch.no_grad():
        pred = model(image)

    scores = list(pred[0]['scores'].detach().cpu().numpy())
    thresholded_preds_inidices = [scores.index(i) for i in scores if i > 0.95]
    thresholded_preds_count = len(thresholded_preds_inidices)

    masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
    masks = masks[:thresholded_preds_count]

    boxes = [[(int(i[0]), int(i[1])), (int(i[2]), int(i[3]))]  for i in pred[0]['boxes'].detach().cpu()]
    boxes = boxes[:thresholded_preds_count]

    labels = []
    for i in pred[0]['labels']:
        for cate in categories:
            if cate['id'] == i:
                labels.append(cate)

    ## draw
    image = draw(orig_image)
    
    # save prediction result
    prefix = "bf16" if args.bf16 else "fp32"
    cv2.imwrite(f"./validate_{prefix}.jpg", image)
