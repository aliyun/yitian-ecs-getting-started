#!/usr/bin/env python
from json import load
import os
import time
import numpy as np
import tensorflow as tf
from tensorflow import dtypes
from tensorflow.python.tools.optimize_for_inference_lib import optimize_for_inference


def load_model(inputs, outputs):
    model_file = "./model/resnet34_tf.22.5.nhwc.pb"
    graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(model_file, "rb") as graph_file:
        graph_def.ParseFromString(graph_file.read())

    optimized_graph_def = optimize_for_inference(graph_def, [item.split(':')[0] for item in inputs],
                [item.split(':')[0] for item in outputs], dtypes.float32.as_datatype_enum, False)
        
    g = tf.compat.v1.import_graph_def(optimized_graph_def, name='')
    return g

if __name__ == "__main__":
    input_shape=(1200,1200)

    ###### image preprocess
    orig_image = tf.keras.preprocessing.image.load_img("./street.jpeg", target_size=input_shape)
    numpy_image = tf.keras.preprocessing.image.img_to_array(orig_image)
    
    mean = np.array([0.485,0.456,0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.22], dtype=np.float32)

    numpy_image = numpy_image / 255.0 - mean
    numpy_image = numpy_image / std

    image_batch = np.expand_dims(numpy_image, axis=0)

    print(image_batch.shape)
    ######

    infer_config = tf.compat.v1.ConfigProto()
    infer_config.intra_op_parallelism_threads = 16
    infer_config.inter_op_parallelism_threads = 2

    inputs = ["image:0"]
    outputs = ["detection_bboxes:0", "detection_classes:0", "detection_scores:0"]

    graph = load_model(inputs, outputs)
    sess = tf.compat.v1.Session(graph=graph, config=infer_config)

    best_time = 1000
    for i in range(6):
        s = time.time()
        predictions = sess.run(outputs, feed_dict={inputs[0]: image_batch})
        e = time.time()
        if best_time > e - s:
            best_time = e - s
        print(f"inference: {e-s} s")

    print(f"best inference time: {best_time:.4f}")
    print("KPI: ssd " + str(10 / best_time))