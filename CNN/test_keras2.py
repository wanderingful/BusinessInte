#coding:utf-8

'''
    GPU run command:
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cnn.py
    CPU run command:
        python cnn.py
'''
#导入各种用到的模块组件
from __future__ import absolute_import
from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
# from six.moves import range
from SIFT.data import load_data
import random, cPickle




#加载数据
data, label = load_data()
#打乱数据
index = [i for i in range(len(data))]
random.shuffle(index)
data = data[index]
data = data/255
label = label[index]
print(data.shape[0], ' samples')
#label为0~19共20个类别，keras要求格式为binary class matrices,转化一下，直接调用keras提供的这个函数
label = np_utils.to_categorical(label, 20)
# print (data)
###############
#开始建立CNN模型
###############

#生成一个model
model = Sequential()


#第一个卷积层，4个卷积核，每个卷积核大小5*5。1表示输入的图片的通道,灰度图为1通道。
#border_mode可以是valid或者full，具体看这里说明：http://deeplearning.net/software/theano/library/tensor/nnet/conv.html#theano.tensor.nnet.conv.conv2d
#激活函数用tanh
#你还可以在model.add(Activation('tanh'))后加上dropout的技巧: model.add(Dropout(0.5))
model.add(Convolution2D(4, 5, 5, border_mode='valid',input_shape=data.shape[-3:])) 
# model.add(Activation('sigmoid'))
model.add(Activation('tanh'))

#第二个卷积层，8个卷积核，每个卷积核大小3*3。4表示输入的特征图个数，等于上一层的卷积核个数
#激活函数用tanh
#采用maxpooling，poolsize为(2,2)
model.add(Convolution2D(8, 3, 3, border_mode='valid'))
model.add(Activation('tanh'))
# model.add(Activation('sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#第三个卷积层，16个卷积核，每个卷积核大小3*3
#激活函数用tanh
#采用maxpooling，poolsize为(2,2)
model.add(Convolution2D(16, 3, 3, border_mode='valid')) 
model.add(Activation('tanh'))
# model.add(Activation('sigmoid'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#全连接层，先将前一层输出的二维特征图flatten为一维的。
#Dense就是隐藏层。16就是上一层输出的特征图个数。4是根据每个卷积层计算出来的：(28-5+1)得到24,(24-3+1)/2得到11，(11-3+1)/2得到4
#全连接有128个神经元节点,初始化方式为normal
model.add(Flatten())
model.add(Dense(128, init='normal'))
model.add(Activation('tanh'))
# model.add(Activation('sigmoid'))

#Softmax分类，输出是20类别
model.add(Dense(20, init='normal'))
model.add(Activation('softmax'))


#############
#开始训练模型
##############
#使用SGD + momentum
#model.compile里的参数loss就是损失函数(目标函数)
sgd = SGD(l2=0.0, lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, class_mode="categorical")
# model.compile(loss='mean_squared_error', optimizer='sgd', class_mode="categorical")

#调用fit方法，就是一个训练过程. 训练的epoch数设为10，batch_size为128．
#数据经过随机打乱shuffle=True。verbose=1，训练过程中输出的信息，0、1、2三种方式都可以，无关紧要。show_accuracy=True，训练时每一个epoch都输出accuracy。
#validation_split=0.2，将20%的数据作为验证集。
hist = model.fit(data, label, batch_size=128, nb_epoch=100, shuffle=True, verbose=1, show_accuracy=True, validation_split=0.0)

