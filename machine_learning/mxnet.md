## 整体介绍

MXNet是基础，Gluon是封装，两者犹如TensorFlow和Keras
静态图Symbolic的代表就是 Tensorflow，我们首先定义好计算图，然后feed数据进行训练网络参数。 即符号式或函数式编程,会进行优化,速度快，省内存，便于线上部署.
动态图Imperative的代表就是 pytorch 和 Gluon，在运行的时候定义图，在每个mini-batch 进行训练的时候都会重新定义一次计算图。
即命令式编程,不会进行优化，类似Python语言能够单部调试


gluon模型的定义方式有sequential类(动态图,能够调试)和HybridSequential类(既支持静态图模式也有动态图模式),
HybridSequential类可以调用hybridize函数来编译和优化实例中串联的层的计算。模型的计算结果不变. 实际是只有继承HybridBlock的层才会被优化, 
而不是HybridSequential类。例如，HybridSequential类和Gluon提供的Dense类都是HybridBlock的子类，
它们都会被优化计算。如果一个层只是继承自Block而不是HybridBlock类，那么它将不会被优化
https://discuss.gluon.ai/t/topic/918/19

sequential和block之间的关系: sequential继承自block,不是将Block叫做层或者模型之类的名字，这是因为它是一个可以自由组建的部件。
它的子类既可以一个层，例如Gluon提供的Dense类，也可以是一个模型，我们定义的MLP类，或者是模型的一个部分，例如ResNet的残差块    
https://www.cnblogs.com/hellcat/p/9046191.html
FeedForward和Module都是进行训练的初始化类, 前者可扩展性小,被弃用.




以mxnet从 0 开始训练模型时,需要先声明模型参数,然后再使用它们来构建模型。但gluon 提供大量预定义的层,我们只需要关注使用哪些层来构建模型.
构建模型最简单的办法是利用 Sequential 来所有层串起来。输入数据之后,Sequential 会依次执行每一层,并将前一层的输出,作为输入提供给后面的层.

梯度概念是建立在偏导数与方向导数概念基础上的,偏导数只能表示多元函数沿某个坐标轴方向的导数,除开沿坐标轴方向上的导数，多元函数在非坐标轴方向上也可以求导数，这种导数称为方向导数。
一个很自然的问题是：在这些方向导数中，是否存在一个最大的方向导数，如果有，其值是否唯一？为了回答这个问题，便需要引入梯度的概念。
梯度可以定义为一个函数的全部偏导数构成的向量(这一点与偏导数与方向导数不同，两者都为标量).事实上，梯度向量的方向即为函数值增长最快的方向

多分类问题中，每个输出的最终要符合概率分布，而softmax函数正好能够做到。softmax函数将输出转化为了概率，交差损失函数则是损失函数的一种计算方法，
它将两个概率分布的负交叉熵作为目标值,最小化这个值等价于最大化这两个概率的相似度。



tensorflow中张量保存的是计算过程而不是数字，有三个属性：名字，类型，维度。tensorflow的计算通过计算图的模型建立，计算图上的每个节点代表了一个计算。计算的结果就保存在张量中。    

正则化的思想是在损失函数中加入刻画模型复杂度的指标，避免过拟合。  泛化误差是整个模型在某一问题上的表现，对新数据的误差。

池化层用于降低分辨率，减小参数规模，不改变输入的深度，有加开计算速度防止过拟合的作用。 卷积层一般使深度加深。卷积层的参数个数和输入的图片大小无关，只和过滤器的尺寸、深度及当前节点矩阵的深度有关。  
卷积核的深度一般比输入的通道大，每经过一层池化层，卷积层过滤器的深度会乘以2.
卷积层的深度的理解： 比如一个3*3*32的卷积层，表示该层卷积有32个filter，输入10*10*3的输出得到的是32层，输入10*10*1的输出也是32层，
每层的输出是用这个filter遍历每个通道卷积的结果。每一个卷积核（filter）学习不同的特征得到不同的 feature map（因为不同卷积核的权值weights是不一样的，计算结果也就不一样，得到的map也自然不同。）
https://blog.csdn.net/jiachen0212/article/details/78459597


fine-tune:
比如大量基于imagenet数据集训练好的模型. 只需要将模型的输出层换成自己的,然后用少量的数据即可训练出好的模型. 深度模型的迁移训练就是这样,
把最后一层替换.  但是最终模型的所有参数都有微调.   还有一种是前面的层的参数都不变,用自己的数据训练的时候只改变输出全连接层的参数.
http://mxnet.incubator.apache.org/faq/finetune.html?highlight=model
https://gluon.mxnet.io/chapter08_computer-vision/fine-tuning.html


在输入神经网络前我们将输入图片直接转成了向量。这样做有两个不好的地方:
• 在图片里相近的像素在向量表示里可能很远,从而模型很难捕获他们的空间关系。
• 对于大图片输入,模型可能会很大。例如输入是 256 × 256 ×3，
输出层是 1000,那么这一层的模型大小是将近 1GB.




## kv-store
kvstore主要是解决你的梯度更新是在cpu进行还是gpu进行
默认是‘device’，表示在GPU上计算梯度和更新权重 在cpu上更新，为‘local’

## attach_grad

在mxnet中，数据、标签、模型参数和超参数由mx.nd.NDArray存储。模型参数记得 NDArray.attach_grad(), 
因为模型参数更新的时候需要用到梯度，attach_grad(). 可以是先有函数关系，然后用attach_grad开辟空间，也可以先with attach_grad()的下定义函数关系。

默认条件下，MXNet不会自动记录和构建用于求导的计算图，我们需要使用autograd里的record()函数来显式的要求MXNet记录我们需要求导的程序。
接下来我们可以通过z.backward()来进行求导。如果z不是一个标量，那么z.backward()等价于nd.sum(z).backward()。即如果batcsize大于1，
会一次行求出所有数据的梯度，那么SGD中跟新梯度时，需要用算出来的总梯度/batchsize*学习率

backward只是计算出梯度，怎么根据这个梯度去更新模型参数就是优化算法做的事，比如随机梯度下降sgd就直接是a-lr*grad/batch-size.
求梯度是对loss(net, input)建立的映射关系求梯度，而不是net建立的关系求梯度。
    
    # 线性回归的实现https://zh.gluon.ai/chapter_deep-learning-basics/linear-regression-scratch.html
    lr = 0.03
    num_epochs = 3
    net = linreg
    loss = squared_loss
    
    for epoch in range(num_epochs):  # 训练模型一共需要num_epochs个迭代周期
        # 在每一个迭代周期中，会使用训练数据集中所有样本一次（假设样本数能够被批量大小整除）。X
        # 和y分别是小批量样本的特征和标签
        for X, y in data_iter(batch_size, features, labels):
            with autograd.record():
                l = loss(net(X, w, b), y)  # l是有关小批量X和y的损失
            l.backward()  # 小批量的损失对模型参数求梯度
            sgd([w, b], lr, batch_size)  # 使用小批量随机梯度下降迭代模型参数
        train_l = loss(net(features, w, b), labels)
        print('epoch %d, loss %f' % (epoch + 1, train_l.mean().asnumpy()))
        
    # 
    求梯度求的是loss函数，net()函数让我们获得output，output和label比较得到loss，相当于loss = square_loss(net(data), label)，
    这就是反应了loss和w,b的关系，因为net是关于w和b的函数，而w和b正是我们要更新的。跟autograd例子里面里面y的作用类似。
    其实这设计到复合函数求导，正是因为我们在with-block里面说明了loss和w,b的关系，loss.backward()才知道如何求导。
    
    loss.backward中是对params的w,b分别求导，loss对w,b求导与loss求和之后再对w,b求导因为求和再对参数分别求导是为了减少计算量

所有的图片跑一轮就是一个epoch，每跑一次是跑batch-size大小的数量，跑完一个epoch或者多个epoch之后用当前的模型与验证集
计算在验证集上的loss,也可统一计算训练集上的loss。验证集的loss只是用于评估，可以打印也可以不打印，并不会修改超参数。

batch-size是一次计算这么多的数据，而不是一张一张计算，计算到batch-size大小再汇总。实质就是向量的运算比如加法的一种方法是，
将这两个向量按元素逐一做标量加法，另一种方法是，将这两个向量直接做矢量加法，结果很明显，后者比前者更省时。
尤其训练过程很多是向量或矩阵操作，一维向量的计算和多维向量的计算过程时间上是一样的，只增加了内存空间。

## softmax
线性回归的输出是连续值，不能做分类，分类场景需要多个输出，softmax就是分类的一种实现，
实质是多个线性回归的组合，每个输出也是连续值，按排列顺序表示每一类的置信度，并对输出做了归一化处理(使用softmax函数)，
使得各个输出之和是1(概率之和)，并且每个输出值的范围都在0-1之间。 这种场景平方损失函数不适合，可使用交叉熵损失函数。

## list
list即序列，一维多维都是序列，切片的方法是一样的，多维的切片就是把一维当做一个元素，逐个切片。
python list中双冒号的使用：序列切片地址可以写为[start：end：step]，其中的开始和结束可以省略，可以只省略其中一个，也可以都省略。
范围是[start,end),如果同时省略了start和end,就是双冒号。当step等于负数的时候，从右向左取数.所以比如a=[1,2,3],则a[::-1]为[3,2,1]

单冒号切片a[start:end]的范围是[start,end),可以省略一个也可以都省略。

list只支持索引和切片访问“ list indices must be integers or slices, not tuple”，不支持取列的操作，
而numpy array是方便支持取列的。所以list要进行取列操作先转成array。

    >>>a=[[1,2,3],[4,5,6]]
    >>> a[0]    #取一行
    [1, 2, 3]
    >>> a[:,0]  # 尝试用numpy array的方法读取一列失败


在list中的数据类型保存的是数据的存放的地址即引用，并非数据，这样可以实现共享，但不足之处就是如果只有一个引用的话浪费空间，而且操作效率低。
例如list1=[1,2,3,4]需要4个指针和四个数据，增加了存储和消耗cpu，而array1=numpy.array([1,2,3,4])只需要存放四个数据，
读取和计算更加方便，因此在做纯数字操作时，建议使用array。

左闭右开是惯例，详见 Accelerated C++ 一书里说到过，如果 a = [3, 5), b = [5, 7)，a + b就直接得到 [3, 7)，很方便。
而且空区间可用[x,x)表示。另外，[0, n)是n个连续整数，例如Python里for _ in range(n) 就会执行n次，很好记。因为x[1,2]中1和2代表索引，1代表第二行，
2代表第三列，通过逗号分隔开，分别表示行和列。而x[1:2,1:3]中1:2是左闭右开，所以代表第二行，1:3也是左闭右开，所以代表第二列和第三列

## Numpy
官方中文文档：https://www.numpy.org.cn/index.html

numpy主要用于多维数组执行数值计算，这类计算主要为矩阵乘法、加法、旋转等，数值微分、积分、差值等，常用于机器学习，
图像处理和计算机图形学和数学任务。

numpy数组是Python数组的扩展，给数组配备了大量的函数和运算符。与Python原生的list不同的是，list可以支持不同类型的元素，
而numpy的array只能是相同类型。numpy中ndarray类型


##　mxnet ndarray

    x = mx.nd.ones((2,3))
    <NDArray 2x3 @cpu(0)>
    
    y=numpy.ndarray([1,2,3])
    <class 'numpy.ndarray'>
    
    
## mxnet.gluon和gluoncv
mxnet.gluon是mxnet实现的一些高级接口， gluocv是社区基于gluon接口对分类，检测，分割等算法基于常用模型和数据集的实现与封装。