import os
import torch
import time
import json
import numpy as np
from PIL import Image
from torchvision.transforms import transforms
from torchvision.models.detection.ssd import ssd300_vgg16, SSD300_VGG16_Weights
import random
import cv2
import argparse


def get_val_data():
    anno_file = "../maskrcnn/data/annotations/instances_val2017.json"
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
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    for i in range(len(boxes)):
        # red_map = np.zeros_like(masks[i]).astype(np.uint8)
        # green_map = np.zeros_like(masks[i]).astype(np.uint8)
        # blue_map = np.zeros_like(masks[i]).astype(np.uint8)

        # # apply a randon color mask to each object
        color = COLORS[random.randrange(0, len(COLORS))]
        # red_map[masks[i] == 1], green_map[masks[i] == 1], blue_map[masks[i] == 1] = color
        # # combine all the masks into a single image
        # segmentation_map = np.stack([red_map, green_map, blue_map], axis=2)
        # #convert the original PIL image into NumPy format
        # convert from RGN to OpenCV BGR format
        # apply mask on the image
        # cv2.addWeighted(image, alpha, segmentation_map, beta, gamma, image)
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
        torch_type = torch.bfloat16
    else:
        torch_type = torch.float32

    file_name, anno_list, categories = get_val_data()

    orig_image = Image.open(os.path.join("../maskrcnn/data/val2017", file_name)).convert('RGB')
    image = orig_image.copy()
    trans = transforms.Compose([
        transforms.ToTensor(),
    ])
    image = trans(image)
    image = image.unsqueeze(0).to(torch_type)

    model = ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT).to(torch_type)

    model.eval()
    with torch.no_grad():
        pred = model(image)

    for i in range(len(pred)):
        for k in pred[i].keys():
            pred[i][k] = pred[i][k].to(torch.float32)

    scores = list(pred[0]['scores'].detach().cpu().numpy())
    thresholded_preds_inidices = [scores.index(i) for i in scores if i > 0.95]
    thresholded_preds_count = len(thresholded_preds_inidices)
    print(f"thresholded_preds_count: {thresholded_preds_count}")
    # masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
    # masks = masks[:thresholded_preds_count]

    boxes = [[(int(i[0]), int(i[1])), (int(i[2]), int(i[3]))]  for i in pred[0]['boxes'].detach().cpu()]
    boxes = boxes[:thresholded_preds_count]
    import ipdb; ipdb.set_trace()

    labels = []
    for i in pred[0]['labels']:
        for cate in categories:
            if cate['id'] == i:
                labels.append(cate)

    ## draw
    image = draw(orig_image)
    
    # visualize the image
    # cv2.imshow('Segmented image', image)
    # cv2.waitKey(0)
    prefix = "bf16" if args.bf16 else "fp32"
    cv2.imwrite(f"./validate_{prefix}.jpg", image)
