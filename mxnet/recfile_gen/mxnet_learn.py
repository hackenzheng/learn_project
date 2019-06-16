import mxnet as mx
record = mx.recordio.MXRecordIO('/home/zhg/tmp2.rec', 'w')
for i in range(5):
    #tmp_str = 'record_' + str(i)
    record.write(b'record_%d' % int(i))
    #record.write(tmp_str)
record.close()

