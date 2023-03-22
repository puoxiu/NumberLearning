import numpy as np
from PIL import Image
import cv2

"""
函数功能: 转为灰度图并转为01矩阵
参数：
    img: 灰度图路径(默认名为text.png)
返回：
    32x32的01矩阵
"""
def auto_pretreatment(img = 'images/text.png'):
    X = []
    Y = []
    im1 = Image.open(img)
    imgi = im1.convert('1')
    im = np.array(imgi)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i, j] == 0:
                im[i, j] = 1
                X.append(j)
                Y.append(i)
            else:
                im[i, j] = 0
    min_X = min(X)-6
    max_X = max(X)+6
    min_Y = min(Y)
    max_Y = max(Y)
    img = imgi.crop((min_X, min_Y, max_X, max_Y)).resize((32, 32))
    img.save('images/text.png')
    im = np.array(img)
    
    return im

"""
函数功能: 将得到的01矩阵存储到测试集中??
参数：
    filename: 得出的32*32矩阵保存位置
    path: 灰度图路径(默认名为text.png)
"""
def save_pic_to_file(filename= './nowDigits/newNumber.txt', path='images/text.png'):
    ret = auto_pretreatment(path)
    np.savetxt(filename, ret, fmt='%d')
    with open(filename) as f:
        num = f.read()
    num = num.replace(' ', '').replace('1', '2').replace('0', '3').replace('2', '0').replace('3', '1')
    # print(num)
    with open(filename, 'w') as f:
        # print(num)
        f.write(num)

if __name__ == '__main__':
    save_pic_to_file('./nowDigits/newNumber.txt', 'images/text.png')
