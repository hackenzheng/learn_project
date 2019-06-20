# -*- coding: utf-8 -*-
import mxnet as mx
import matplotlib.pylab as plt

# train_data = mx.recordio.MXRecordIO('./debug.rec', 'r')
# train_data = mx.recordio.MXRecordIO('./voc-1154.rec', 'r')
train_data = mx.recordio.MXRecordIO('./yibao-2.rec', 'r')
ret = []
for i in range(10):
    item = train_data.read()
    if not item:
        break
    print(i)
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
