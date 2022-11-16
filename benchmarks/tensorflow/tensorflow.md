# Tensorflow workload

Our workloads demonstrate how to run inference using tensorflow.

We select four common inference scenarios, covering image classification and recognition, object detection, natural language processing, and recommendation system. The representative models used are as follows:

| Area | Task | Model |
| ---- | ---- | ----- |
| Vision | Image Classification	| Resnet50-v1.5 and VGG19
| Vision | Object Detection	| SSD-Resnet34
| Language | Natural Language Processing | BERT-Large
| Recommendation | Click-Through Rate Prediction | DIN

Resnet, SSD and BERT are all from the [MLPerf Inference Benchmark](https://github.com/mlcommons/inference) project. [DIN](https://github.com/zhougr1993/DeepInterestNetwork) is the click-through rate prediction model proposed by Alibaba.


## Downloading an image from Docker Hub
Completed images can be pulled from [cape2/tensorflow](https://hub.docker.com/r/cape2/tensorflow).

```bash
docker pull cape2/tensorflow:latest
```

## Runing the Image

Run on different platforms (Yitian, Icelake, Ampere etc.) to compare the inference results:

```bash
docker run --rm cape2/tensorflow:latest
```

