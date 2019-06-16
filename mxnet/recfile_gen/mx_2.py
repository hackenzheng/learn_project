import mxnet as mx
record = mx.recordio.MXIndexedRecordIO('/home/zhg/tmp.idx', '/home/zhg/tmp.rec', 'w')
for i in range(5):
    record.write_idx(i, b'record_%d'%i)
record.close()
