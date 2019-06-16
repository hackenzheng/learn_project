import mxnet as mx
import matplotlib.pyplot as plt
import numpy as np
data_iter = mx.io.ImageRecordIter(batch_size=4, 
                              resize=60,
                              label_width = 20,
                              data_shape=(3, 60, 60),# depth,height,width
                              path_imgrec="val.rec",
                              path_imgidx="val.idx" )
                              #path_imgrec="~/intellif/code_zhg/fast-learner/flbackend/flinference/img/val.rec",
                              #path_imgidx="~/intellif/code_zhg/fast-learner/flbackend/flinference/img/val.idx" )
data_iter.reset()
batch = data_iter.next()
data = batch.data[0]
for i in range(4):
    plt.subplot(1,4,i+1)
    plt.imshow(data[i].asnumpy().astype(np.uint8).transpose((1,2,0)))
plt.show()
