# -*- coding: utf-8 -*-

import logging
import mxnet as mx
import numpy as np
from mxnet import nd
import argparse
import matplotlib.pylab as plt
import os
import cv2
import matplotlib.image as mpimg
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)
logging.info('start to train')

train_path = os.path.split(os.path.realpath(__file__))[0] + '/cifar/train.rec'
val_path = os.path.split(os.path.realpath(__file__))[0] + '/cifar/test.rec'
prefix = os.path.split(os.path.realpath(__file__))[0] + '/image-classifier-resnet101_v1'
batch_size = 128
epoch = 10


train_data = mx.recordio.MXRecordIO('./cifar/test.rec', 'r')
ret = []
for i in range(200):
    item = train_data.read()
    if not item:
        break

    header, img_arr = mx.recordio.unpack_img(item)
    print(header)
    ret.append((header, img_arr))
    plt.imshow(img_arr)
    plt.show()

    # print(img_arr.shape)
    # print(help(img_arr.resize))
    # img_arr.resize((16,16,3), refcheck=True)
    # print(img_arr)

    #tmp = mx.image.imresize(img_arr.asarray, 100, 70)
    #plt.imshow(tmp.asnumpy())
    # plt.imshow(img_arr)
    # plt.show()


record = mx.recordio.MXRecordIO('./cifar/test_200.rec', 'w')
for i in range(len(ret)):
    header, img_arr = ret[i]
    #header = mx.recordio.IRHeader(flag=i., label=[], id=header.id, id2=0)
    s = mx.recordio.pack_img(header, img_arr)
    record.write(s)



"""
# load train data and test data
train_data = mx.io.ImageRecordIter(
    path_imgrec=train_path,
    path_imgidx='',
    label_width=1,
    preprocess_threads=4,
    data_name='data',
    label_name='softmax_label',
    shuffle=True,
    data_shape=(3, 32, 32),
    batch_size=batch_size,
)


img_data = train_data.getdata()[0]
plt.imshow(img_data.asnumpy().astype(np.uint8).transpose((1,2,0)))
plt.show()

label_list = train_data.getlabel()
print(label_list)

#print(train_data.getdata())
print('index====')
print(train_data.getindex())
print('label====')
print(len(train_data.getlabel()))
#print(train_data.next())
print(train_data.provide_data)
#print(train_data.label)
"""




