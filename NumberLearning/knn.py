import numpy as np
import operator
from os import listdir

"""
函数说明:kNN算法,分类器
Parameters:
	inX - 用于分类的数据(测试集)
	dataSet - 用于训练的数据(训练集)
	labes - 分类标签
	k - kNN算法参数,选择距离最小的k个点
Returns:
	sortedClassCount[0][0] - 分类结果
"""
def classify(inX, dataSet, labels, k):
	#numpy函数shape[0]返回dataSet的行数
	dataSetSize = dataSet.shape[0]

	#在列向量方向上复制inX共1次(横向),行向量方向上复制inX共dataSetSize次(纵向)--使得测试数据转化为与训练数据相等行列的矩阵形式
    # 例如 intX = [42,3] dataSetSize = 4
    # 则有 diffMat = [[42,3],[42,3],[42,3],[42,3]]
	diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
	#二维特征相减后平方
	sqDiffMat = diffMat**2
	#sum()所有元素相加,sum(0)列相加,sum(1)行相加
	sqDistances = sqDiffMat.sum(axis=1)
	#开方,计算出欧式距离
	distances = sqDistances**0.5
	#返回distances中元素从小到大排序后的索引值
	sortedDistIndices = distances.argsort()
	#定一个记录类别次数的字典
	classCount = {}
	for i in range(k):
		#取出前k个元素的类别
		voteIlabel = labels[sortedDistIndices[i]]
		#dict.get(key,default=None),字典的get()方法,返回指定键的值,如果值不在字典中返回默认值。
		#计算类别次数
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
	#python3中用items()替换python2中的iteritems()
	#key=operator.itemgetter(1)根据字典的值进行排序
	#key=operator.itemgetter(0)根据字典的键进行排序
	#reverse降序排序字典
	sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
	#返回次数最多的类别,即所要分类的类别
	return sortedClassCount[0][0]

"""
函数说明:将图像数据处理为一个向量: 将32*32的二进制图像信息转化为1*1024的向量 再使用前面的分类算法
Parameters:
	filename - 文件名
Returns:
	returnVect - 返回的二进制图像的1x1024向量
"""
def img2vector(filename):
	#创建1x1024零向量
	returnVect = np.zeros((1, 1024))
	#打开文件
	fr = open(filename)
	#按行读取
	for i in range(32):
		#读一行数据
		lineStr = fr.readline()
		#每一行的前32个元素依次添加到returnVect中
		for j in range(32):
			returnVect[0, 32*i+j] = int(lineStr[j])
	#返回转换后的1x1024向量
	return returnVect

"""
函数说明:导入训练数据
parameters:
    filename: 数据文件路径
return:
    数据矩阵 returnMat 和对应的类别 classLabelVector
"""
def file2matrix(filename= './trainingDigits'):
    classLabelVector = [] # 生成返回的标签向量
    # 获得训练样本文件夹中的数据集
    trainingFileList = listdir(filename)
    # 样本数的个数
    m = len(trainingFileList)
    # 返回m行1024列的矩阵数据
    returnMat = np.zeros((m, 1024))
    # 根据文件名得出标签， 下划线左边的数字是标签
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split(".")[0]
        # 分类标签
        classNumStr = int(fileStr.split('_')[0])
        classLabelVector.append(classNumStr)
        returnMat[i, :] = img2vector('trainingDigits/%s' % fileNameStr)
    # 返回数据矩阵returnMat和对应的类别classLabelVector
    return returnMat, classLabelVector

"""
手写数字分类测试, 测试集,
返回 errorCount错误次数, errorRate 错误率
"""
def numberClassifyTest(k= 3):
	# 获得训练集矩阵 及每个特征所对应标签
	trainingMat, classLabelVector = file2matrix()

	# 返回testDigits文件目录下的文件名列表
	testSetList = listdir('testDigits')
	# 测试数据的数量
	mTest = len(testSetList)
	# 检测错误的数量
	errorCount = 0.0
	# 错误率
	errorRate = 0.0
	# 从文件中解析出测试集的类别并进行分类测试
	for i in range(mTest):
		# 获得文件名
		fileName = testSetList[i]
		# 通过文件名获取真实数字--用来对比是否正确
		classNumber = int(fileName.split('_')[0])
		# 获得测试集的1x1024向量,用于训练
		vectorUnderTest = img2vector('testDigits/%s' % (fileName))
		# 获得预测结果
		classifyRes = classify(vectorUnderTest, trainingMat,classLabelVector,k)
		# 结果处理
		if classifyRes != classNumber:
			errorCount += 1.0
		# 错误率
		errorRate = errorCount / mTest
		# print("KNN分类返回结果为%d\t,真实结果为%d" % (classifyRes, classNumber))
	# print("总共错误了%d个,错误率为%f%%" % (errorCount, errorRate))

	return errorCount,errorRate

"""
识别函数: 识别新生成的32*32矩阵,得出识别结果并返回
"""
def discriminateInput(fileName='./nowDigits/newNumber.txt',k = 3):
	print("正在进行数字识别！")
	# 读取文件filename中的32*32矩阵，并转为1*1024矩阵
	newImMetric = img2vector(fileName)
	# 获得训练集矩阵 及每个特征所对应标签
	trainingMat, classLabelVector = file2matrix()
	# 获得预测结果
	classifyRes = classify(newImMetric, trainingMat,classLabelVector,k)
	
	print("本次识别结果为：",classifyRes)

	return classifyRes


if __name__ == '__main__':
	numberClassifyTest(3)
	# discriminateInput()