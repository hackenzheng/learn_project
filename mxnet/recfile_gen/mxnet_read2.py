import mxnet as mx
import matplotlib.pyplot as plt
import numpy as np

data_iter = mx.image.ImageIter(batch_size=4, data_shape=(3, 500, 500),
                              path_imgrec="mydata.rec",
                              path_imgidx="mydata.idx" )
data_iter.reset()
batch = data_iter.next()
data = batch.data[0]
for i in range(4):
    plt.subplot(1,4,i+1)
    plt.imshow(data[i].asnumpy().astype(np.uint8).transpose((1,2,0)))
plt.show()
