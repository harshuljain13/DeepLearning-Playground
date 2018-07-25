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

data_dir = '../../../data/NIST19/'

img_size = 128
flatten_img_size = img_size*img_size
num_channels = 3
img_shape = (img_size,img_size,num_channels)
num_classes = 62

# making the maps [alternative is to load it from saved json]
label_cls_name_map = {}

with open('../../OCR/label_cls_name.json', 'r') as f:
    label_cls_json = f.read()

label_cls_name_map = json.loads(label_cls_json)

def get_predictions(image_np):
    tf.reset_default_graph()
    x = tf.placeholder(tf.float32, shape=[None, img_size, img_size, num_channels], name='x')
    conv1 = tf.layers.conv2d(inputs=x, name='layer_conv1', padding='same', filters=32, kernel_size=5, 
                             activation=tf.nn.relu)
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=2, strides=2)
    conv2 = tf.layers.conv2d(inputs=pool1, name='layer_conv2', padding='same', filters=64, kernel_size=5, 
                             activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=2, strides=2)
    layer3 = tf.contrib.layers.flatten(pool2)
    fc1 = tf.layers.dense(inputs=layer3, name='layer_fc1', units=512, activation=tf.nn.relu)
    fc2 = tf.layers.dense(inputs=fc1, name='layer_fc2', units=256, activation=tf.nn.relu)
    net = tf.layers.dense(inputs=fc2, name='layer_fc_out', units=num_classes, activation=None)

    logits = net
    y_pred = tf.nn.softmax(logits=logits)
    y_pred_cls = tf.argmax(y_pred, dimension=1)
    
    session = tf.Session()

    # loading the saved model from the checkpoints directory
    session.run(tf.global_variables_initializer())
    #saver= tf.train.Saver()
    #saver.restore(sess=session, save_path='../../OCR/best_validation')
    shape_ = image_np.shape
    feed_dict = {x: np.reshape(image_np, (1, shape_[0], shape_[1], shape_[2]))}
    y_pred_ = session.run(y_pred, feed_dict=feed_dict)
    y_pred_ = np.squeeze(y_pred_)
    y_pred_cls_ = np.argmax(y_pred_)
    class_name = label_cls_name_map[str(y_pred_cls_)]
    session.close()

    return class_name