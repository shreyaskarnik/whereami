import collections
import logging
import os
import urllib

import numpy as np

import mxnet as mx
import utils
from skimage import io, transform

MODEL_PATH = os.getenv("MODEL_PATH", "/opt/ml/model/")
MODEL_NAME = os.getenv("MODEL_NAME", "RN101-5k500")

sym, arg_params, aux_params = mx.model.load_checkpoint(
    MODEL_PATH + MODEL_NAME, 12)
mod = mx.mod.Module(symbol=sym, context=mx.cpu())
mod.bind([('data', (1, 3, 224, 224))], for_training=False)
mod.set_params(arg_params, aux_params, allow_missing=True)

mean_rgb = np.array([123.68, 116.779, 103.939]).reshape((3, 1, 1))

Batch = collections.namedtuple('Batch', ['data'])
grids = []

with open('grids.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        lat = float(line[1])
        lng = float(line[2])
        grids.append((lat, lng))


def download_image(url):
    logging.info("downloading {}".format(url))
    fd = urllib.urlopen(url)
    img = io.call_plugin('imread', fd, plugin='pil')
    return img


def preprocess_image(img):
    logging.info("preprocessing image")
    # We crop image from center to get size 224x224.
    short_side = min(img.shape[:2])
    yy = int((img.shape[0] - short_side) / 2)
    xx = int((img.shape[1] - short_side) / 2)
    crop_img = img[yy: yy + short_side, xx: xx + short_side]
    resized_img = transform.resize(crop_img, (224, 224))
    # convert to numpy.ndarray
    sample = np.asarray(resized_img) * 256
    # swap axes to make image from (224, 224, 3) to (3, 224, 224)
    sample = np.swapaxes(sample, 0, 2)
    sample = np.swapaxes(sample, 1, 2)
    # sub mean
    normed_img = sample - mean_rgb
    normed_img = normed_img.reshape((1, 3, 224, 224))
    return [mx.nd.array(normed_img)]


def predict(img, max_predictions):
    logging.info("predicting")
    mod.forward(Batch(img), is_train=False)
    prob = mod.get_outputs()[0].asnumpy()[0]
    pred = np.argsort(prob)[::-1]
    raw_result = []
    for i in range(max_predictions):
        raw_result.append(grids[int(pred[i])])
    return utils.geocode(raw_result)


def download_and_predict(url, max_predictions=3):
    logging.info("invoking")
    img = preprocess_image(download_image(url))
    return predict(img, max_predictions)
