
import os,io
import shutil

helm_app = 'prometheus'

# 执行命令获取返回值
status = os.popen("helm install --dry-run --debug "+helm_app)
result = status.read()
status.close()
# print(result)

# 正则匹配输出文件
canwrite=False
nowpath = ""
nowfile=None
allline = result.split('\n')
if os.path.exists('new'):
    shutil.rmtree('new')
for line in allline:
    if(line.startswith('# Source: ')):
        if (nowpath):
            nowfile.close()

        nowpath = 'new/'+line.replace('# Source: ','')
        nowdir = os.path.dirname(nowpath)
        if(not os.path.exists(nowdir)):
            os.makedirs(nowdir)
        nowfile=open(nowpath,mode='w')
        canwrite=True

    if (canwrite and nowpath and nowfile):
        nowfile.write(line+"\n")

    print(line)






