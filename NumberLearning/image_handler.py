from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PIL import  ImageGrab
import os

import image_to_grey

# 因为此ui要作为子窗口被调用，所以要修改继承的类
class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.resize(1920, 1080)

        # 创建QPoint类型的数据，因为pyqt监听鼠标事件返回的坐标点是Qpoint类型
        self.firstPoint = QtCore.QPoint()
        self.endPoint = QtCore.QPoint()

        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint) #让窗口显示在屏幕的最上层
        self.setWindowState(QtCore.Qt.WindowFullScreen)  # 窗口全屏幕

    # 设置画图事件
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # QPainter是在窗体中用来绘制的类
        paint = QtGui.QPainter(self)
        # 把图片绘制到窗体中，前两个0表示图片相对窗体左上角的位置，这里设置0，0为了让窗体全屏幕显示
        paint.drawPixmap(0, 0, QtGui.QPixmap('./images/screen.png'))
        # 设置绘图时画笔的颜色
        paint.setPen(QtCore.Qt.red)
        # 绘制矩形的方法，其中的参数来自鼠标事件
        paint.drawRect(self.firstPoint.x(), self.firstPoint.y(), self.endPoint.x() - self.firstPoint.x(),
                       self.endPoint.y() - self.firstPoint.y())

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.firstPoint = a0.pos()
        # print(self.firstPoint)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.endPoint = a0.pos()
        self.update()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.endPoint = a0.pos()
        self.update()
        # 这里截图需要注意一点，前两个参数都进行了加一个像素单位的处理，目的是为了截图完成后排除画笔画出来的矩形边框
        im = ImageGrab.grab((self.firstPoint.x()+1 , self.firstPoint.y()+1 , self.endPoint.x(), self.endPoint.y()))
        im.save("./images/text.png")
        
        # image_to_grey.transf("./images/text.png")

        os.remove('./images/screen.png')
        # 截图完成后退出窗体
        self.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(723, 491)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 723, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = Ui_MainWindow()
    w.show()
    app.exec_()
