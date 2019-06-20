import mxnet as mx
import cv2
import os

# 将rec文件解压，保存png图片

rec = mx.recordio.MXRecordIO("val-5k-256.rec", "r")
root_path = "./image"
try:
    for i in range(10):
        print(i)
        item = rec.read()
        _, img = mx.recordio.unpack_img(item)

        tmp = os.path.join(root_path, "{}.png".format(i))
        print(tmp)
        cv2.imwrite(tmp, img)  # 没有权限写不会报错，要先创建好目录，不会自动创建，不事先创建目录也不会报错
        # cv2.imwrite('./image/2.png', img)
        # cv2.imencode('.jpg', img)[1].tofile('./1.jpg') # 也可以保存
        #cv2.imshow("image", img)  # 显示图片
        # cv2.waitKey(0)
    rec.close()
except Exception as e:
    print(e)
