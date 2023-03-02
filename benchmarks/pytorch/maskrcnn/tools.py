import os
import json
import urllib.request


def downloads_image(num: int):
    with open("./data/annotations/captions_val2017.json") as f:
        info = json.load(f)
    for i in range(num):
        img_url = info["images"][i]["coco_url"]
        img_name = info["images"][i]["file_name"]
        urllib.request.urlretrieve(img_url, os.path.join("./data/val2017", img_name))


if __name__ == "__main__":
    downloads_image(4)
