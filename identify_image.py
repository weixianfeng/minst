from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf


def train_sess():
    # Import data
    mnist = input_data.read_data_sets('.', one_hot=True)

    # Create the model
    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.matmul(x, W) + b

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, 10])

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    # Train
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    return x, y, sess


def image2arr(filename):
    arr = []
    img = Image.open(filename)
    img = img.convert("1")
    pixel = img.load()
    width, height = img.size
    for x in range(0, width):
        for y in range(0, height):
            arr.append(pixel[y, x] / 255)
    return arr


def get_code(filename):
    arr = image2arr(filename)
    y_pre = sess.run(y, feed_dict={
        x: [arr]
    })
    return np.argmax(y_pre[0])


x, y, sess = train_sess()
