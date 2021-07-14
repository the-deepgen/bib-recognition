#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf
import tensorflow.keras as kr
from keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Input
from tensorflow.keras import Model
from tensorflow.keras.regularizers import l2


class Ssd(Model):

    def __init__(self, config):
        super(Ssd, self).__init__()
        self.config = config
        input_shape = (config["input_size"], config["input_size"], 3)
        # construct the base network and extra feature layers
        base_network = VGG16(
            input_shape=input_shape,
            classes=config.get("num_classes", 1),
            weights='imagenet',
            include_top=False
        )
        base_network = Model(inputs=base_network.input, outputs=base_network.get_layer('block5_conv3').output)
        base_network.get_layer("input_1")._name = "input"
        for layer in base_network.layers:
            if "pool" in layer.name:
                new_name = layer.name.replace("block", "")
                new_name = new_name.split("_")
                new_name = f"{new_name[1]}{new_name[0]}"
            else:
                new_name = layer.name.replace("conv", "")
                new_name = new_name.replace("block", "conv")
            base_network.get_layer(layer.name)._name = new_name
            base_network.get_layer(layer.name)._kernel_initializer = "he_normal"
            base_network.get_layer(layer.name)._kernel_regularizer = l2(config["l2_regularization"])
            layer.trainable = False
