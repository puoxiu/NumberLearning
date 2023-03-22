from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import  ImageGrab
import sys
import shutil

import knn
import image_handler

import number_to_01

"""
复制文件到images文件夹下,等待被处理
fileName: 文件路径
copyName: 复制后的文件名
"""
def copy_file(fileName,copyName = './images/src.png'):
    shutil.copy(fileName, copyName)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.layout_ui()
        self.set_signal_plot()

        # 防止重复对一张图片二值化
        self.first = False

    # 窗口初始化
    def init_ui(self):
        self.setWindowTitle("手写数字识别系统.01 version")
        center_pointer = QDesktopWidget().availableGeometry().center()
        x = center_pointer.x() / 2 + 100
        y = center_pointer.y() / 2 - 150
        self.move(x,y)
        self.resize(1100,800)
    # 窗口布局
    def layout_ui(self):
        # 最外层布局三部分：菜单、图片区域、结果打印区域
        container = QVBoxLayout()

        # -----创建第1个组------菜单-------
        menu_box = QGroupBox()
        # menu_layout 保证三个爱好是垂直摆放
        menu_layout = QHBoxLayout()
        self.btn1 = QPushButton("选择图片")
        self.btn2 = QPushButton("裁剪")
        self.btn3 = QPushButton("开始识别")
        self.btn4 = QPushButton("测试集")
        # 添加到menu_layout中
        menu_layout.addWidget(self.btn1)
        menu_layout.addWidget(self.btn2)
        menu_layout.addWidget(self.btn3)
        menu_layout.addWidget(self.btn4)
        # 把menu_layout添加到menu_box中
        menu_box.setLayout(menu_layout)

        # image_layout = QHBoxLayout()
        # label1 = QLabel()
        # label1.setText("   显示图片")
        # label1.setFixedSize(300, 200)
        # image_layout.addWidget(label1)

        # -----创建第2个组--图片显示-----
        # 图片显示组
        image_box = QGroupBox()
        # 图片容器
        image_layout = QHBoxLayout()
        # 
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label1.setText("                                               显示初始图")
        self.label2.setText("                                               显示灰度图")

        self.label1.setFixedSize(500, 400)
        self.label2.setFixedSize(500, 400)

        # 追加到图片容器中
        image_layout.addWidget(self.label1)
        image_layout.addWidget(self.label2)
        # 添加到 box中
        image_box.setLayout(image_layout)


        # -----创建第3个组----计算结果-----
        res_box = QGroupBox()
        res_layout = QHBoxLayout()
        self.res_browser = QTextBrowser()
        self.res_browser.setText("结果显示")
        res_layout.addWidget(self.res_browser)
        res_box.setLayout(res_layout)

        container.addWidget(menu_box)
        container.addWidget(image_box)
        container.addWidget(res_box)

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        pass
    
    # 设置信号与槽
    def set_signal_plot(self):
        self.btn1.clicked.connect(self.select_image)
        self.btn2.clicked.connect(self.cut_image)
        self.btn3.clicked.connect(self.discriminate)
        self.btn4.clicked.connect(self.testDigit)
    # 选择图片文件
    def select_image(self):
        print("选择图片")
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.png;;*.jpg;;All Files(*)")
        if imgName :
            # 将选择的图片复制到images/文件夹下
            copy_file(imgName)
            png = QPixmap(imgName).scaled(self.label1.width(), self.label1.height())
            # png = QPixmap(imgName).scaled(200,200)
            self.label1.setPixmap(png)
        else :
            self.res_browser.setPlainText("未选择图片")

    # 截图--
    def cut_image(self):
        try:
            # 获取全屏截图并保存
            img = ImageGrab.grab()
            img.save('./images/screen.png')
            self.child_window = image_handler.Ui_MainWindow()
            self.child_window.show()
            # self.showNormal()
            # 标记首次识别图片
            self.first = True
        except:
            pass
    
    # 开始识别
    def discriminate(self):
        # 得到识别图片的32*32的01矩阵，并保存在./nowNumber.txt文件中
        if self.first:
            number_to_01.save_pic_to_file()
            # 显示生成的灰度图
            png = QPixmap('./images/text.png').scaled(self.label2.width(), self.label2.height())
            self.label2.setPixmap(png)
            self.first = False
        res = knn.discriminateInput(k = 3)
        self.res_browser.setText(f"本次识别的结果为：{res}")
    
    # 测试集
    def testDigit(self):
        self.res_browser.setText("正在测试")
        errorCount,errorRate = knn.numberClassifyTest()
        self.res_browser.setText(f"测试错误次数为：{errorCount}\n测试错误率为: {errorRate}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.show()

    app.exec()
