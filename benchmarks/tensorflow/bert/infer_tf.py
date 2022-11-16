import os
import time
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

from squad_QSL import get_squad_QSL


if __name__ == "__main__":
    print("Loading TF model...")
    infer_config = tf.compat.v1.ConfigProto()
    infer_config.intra_op_parallelism_threads = int(os.environ['TF_INTRA_OP_PARALLELISM_THREADS']) \
            if 'TF_INTRA_OP_PARALLELISM_THREADS' in os.environ else os.cpu_count()
    infer_config.inter_op_parallelism_threads = int(os.environ['TF_INTER_OP_PARALLELISM_THREADS']) \
            if 'TF_INTER_OP_PARALLELISM_THREADS' in os.environ else os.cpu_count()
    infer_config.use_per_session_threads = 1
    sess = tf.compat.v1.Session(config=infer_config)

    with gfile.FastGFile('model/model.pb', 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')
    
    qsl = get_squad_QSL()

    best_time = 1000
    for i in range(10):
        eval_features = qsl.get_features(i)
        input_ids   = np.array([eval_features.input_ids])
        input_mask  = np.array([eval_features.input_mask])
        segment_ids = np.array([eval_features.segment_ids])
        feeds = {
            'input_ids:0':   input_ids,
            'input_mask:0':  input_mask,
            'segment_ids:0': segment_ids
        }

        s = time.time()
        sess.run(["logits:0"], feed_dict=feeds)
        e = time.time()
        if best_time > e - s:
            best_time = e - s
        print(f"inference: {e-s} s")

    print(f"best inference time: {best_time:.4f}")
    print("KPI: bert " + str(10 / best_time))