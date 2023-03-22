import cv2

# 将图片黑白二值化
def transf(filename = './images/text.png'):
    #read image
    img_grey = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    # define a threshold, 128 is the middle of black and white in grey scale
    thresh = 128
    # assign blue channel to zeros
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
    #save image
    cv2.imwrite(filename,img_binary)

if __name__ == '__main__':
    transf()
