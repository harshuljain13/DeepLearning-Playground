import pandas as pd
import numpy as np
import tensorflow as tf
import os
import json
import re
import cv2
from keras.utils.np_utils import to_categorical  
import h5py
import sys

data_dir = '../../data/dogs/Images/'

img_size = 299
flatten_img_size = img_size*img_size
img_shape = (img_size,img_size,3)
num_channels = 3
num_classes = 120

# making the maps [alternative is to load it from saved json]
label_cls_name_map = {}

with open('../../dogs_classification/dogs_checkpoints/label_cls_name.json', 'r') as f:
    label_cls_json = f.read()

label_cls_name_map = json.loads(label_cls_json)

def transfer_values(image_np):
    # inception layer
    tf.reset_default_graph()
    inception_dir = '../../data/inception'
    path_uid_to_cls = "imagenet_2012_challenge_label_map_proto.pbtxt"
    path_uid_to_name = "imagenet_synset_to_human_label_map.txt"
    path_graph_def = "classify_image_graph_def.pb"

    uid_cls = {}
    cls_uid = {}
    uid_name = {}

    print os.getcwd()
    with open(os.path.join(inception_dir, path_uid_to_name), mode='r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            elements = line.split("\t")
            uid = elements[0]
            name = elements[1]
            uid_name[uid] = name
        
    with open(os.path.join(inception_dir, path_uid_to_cls), mode='r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("  target_class: "):
                elements = line.split(": ")
                cls_ = int(elements[1])
            elif line.startswith("  target_class_string: "):
                elements = line.split(": ")
                uid = elements[1]
                uid = uid[1:-2]
                uid_cls[uid] = cls_
                cls_uid[cls_] = uid
            
    tensor_name_input_jpeg = "DecodeJpeg/contents:0"
    tensor_name_input_image = "DecodeJpeg:0"
    tensor_name_resized_image = "ResizeBilinear:0"
    tensor_name_softmax = "softmax:0"
    tensor_name_softmax_logits = "softmax/logits:0"
    tensor_name_transfer_layer = "pool_3:0"

    graph = tf.Graph()
    with graph.as_default():
        graph_path = path_graph_def
        with tf.gfile.FastGFile(os.path.join(inception_dir, graph_path), 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')

    y_pred_inception = graph.get_tensor_by_name(tensor_name_softmax)
    y_pred_logits_inception = graph.get_tensor_by_name(tensor_name_softmax_logits)
    transfer_layer = graph.get_tensor_by_name(tensor_name_transfer_layer)
    transfer_layer_len = transfer_layer.get_shape()[3]
    resized_image = graph.get_tensor_by_name(tensor_name_resized_image)
    inception_session = tf.Session(graph=graph)
    print('Processing image of shape : ', image_np.shape)
    feed_dict = {tensor_name_input_image: image_np}
    print(inception_session)
    transfer_values = np.squeeze(inception_session.run(transfer_layer, feed_dict=feed_dict))
    inception_session.close()
    print transfer_values
    return transfer_values, transfer_layer_len

def get_predictions(transfer_values, transfer_layer_len):
    # transfer learning model beyond freezed layers
    tf.reset_default_graph()
    
    x = tf.placeholder(tf.float32, shape=[None, transfer_layer_len], name='x')
    fc1 = tf.layers.dense(inputs=x, name='layer_fc1', units=1024, activation=tf.nn.relu)
    fc2 = tf.layers.dense(inputs=fc1, name='layer_fc2', units=512, activation=tf.nn.relu)
    fc3 = tf.layers.dense(inputs=fc2, name='layer_fc3', units=256, activation=tf.nn.relu)
    
    logits = tf.layers.dense(inputs=fc3, name='layer_fc_out', units=num_classes, activation=None)
    
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
    y_true_cls = tf.argmax(y_true, axis=1)

    y_pred = tf.nn.softmax(logits=logits)
    y_pred_cls = tf.argmax(y_pred, dimension=1)
    session = tf.Session()

    # loading the saved model from the checkpoints directory
    session.run(tf.global_variables_initializer())
    saver= tf.train.Saver()
    saver.restore(sess=session, save_path='../../dogs_classification/dogs_checkpoints/best_validation')
    feed_dict = {x: transfer_values.reshape(1,-1)}
    y_pred_ = session.run(y_pred, feed_dict=feed_dict)
    y_pred_ = np.squeeze(y_pred_)
    y_pred_cls_ = np.argmax(y_pred_)
    class_name = label_cls_name_map[str(y_pred_cls_)]
    session.close()

    return class_name