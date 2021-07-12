#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf
# load the VGG16 network, ensuring the head FC layers are left off
from keras import Input, Model
from keras.applications.vgg16 import VGG16
from keras.layers import Flatten, Dense


class MLP(tf.keras.layers.Layer):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers):
        super(MLP, self).__init__()
        self.num_layers = num_layers
        h = [hidden_dim] * (num_layers - 1)
        self.layers = nn.ModuleList(nn.Linear(n, k) for n, k in zip([input_dim] + h, h + [output_dim]))


def build(self, input_shape):
    self.kernel = self.add_weight("kernel",
                                  shape=[int(input_shape[-1]),
                                         self.num_outputs])


def call(self, inputs):
    return tf.matmul(inputs, self.kernel)


vgg = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))

# freeze all VGG layers so they will *not* be updated during the
# training process
vgg.trainable = False

# flatten the max-pooling output of VGG
flatten = vgg.output
flatten = Flatten()(flatten)

# construct a fully-connected layer header to output the predicted
# bounding box coordinates
bboxHead = Dense(128, activation="relu")(flatten)
bboxHead = Dense(64, activation="relu")(bboxHead)
bboxHead = Dense(32, activation="relu")(bboxHead)
bboxHead = Dense(4, activation="sigmoid", name="bounding_box")(bboxHead)

"""

class MLP(nn.Module):

    def __init__(self, input_dim, hidden_dim, output_dim, num_layers):
        super().__init__()
        self.num_layers = num_layers
        h = [hidden_dim] * (num_layers - 1)
        self.layers = nn.ModuleList(nn.Linear(n, k) for n, k in zip([input_dim] + h, h + [output_dim]))

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = F.relu(layer(x)) if i < self.num_layers - 1 else layer(x)
        return x

      "ymin": 418,
      "xmin": 131,
      "ymax": 478,
      "xmax": 205
      
      Image
      	|  
      VGG16
      	|
      	Flatten
      	|
      	Dense 128
      	|
      	Dense 64
      	|
      	Dense 32
      	|			|		|		|		|		|
      	Dense 4	Dense 4	Dense 4	Dense 4	Dense 4	Dense 4
      
"""
# put together our model which accept an input image and then output
# bounding box coordinates and a class label
model = Model(inputs=vgg.input, outputs=bboxHead)
