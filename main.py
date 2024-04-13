#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QFileDialog
    )

from PIL import Image
from PIL import ImageFilter

import os

#классы
class ImageProcessor():
    def __init__(self):
        self.image = None
        #self.dir = None
        self.filename = None
        self.save_dir = "NewFiles/"
    
    def clear(self):
        self.image = None
        self.dir = None
        self.filename = None

    def loadImage(self, dir, filename):
        self.dir = dir #сохраняем путь к папке
        self.filename = filename #сохраняем имя файла
        image_path = os.path.join(dir, filename) #клеим путь к файлу
        self.image = Image.open(image_path) #загружаем файл

    def showImage(self, path):
        Ib_image.hide()
        pixmapimage = QPixmap(path)
        w, h = Ib_image.width(), Ib_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        Ib_image.setPixmap(pixmapimage)
        Ib_image.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)    

    def do_bw(self):
        try:
            self.image = self.image.convert('L')
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            Ib_image.setText('Вы не выбрали папку или фото')

    def do_flip(self):
        try:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            Ib_image.setText('Вы не выбрали папку или фото')

    def do_right(self): #поворот на право на 90◦
        try:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            Ib_image.setText('Вы не выбрали папку или фото')

    def do_left(self): #поворот на лево на 90◦
        try:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            Ib_image.setText('Вы не выбрали папку или фото')

    def do_blur(self): #резкость
        try:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            Ib_image.setText('Вы не выбрали папку или фото')
#функции
def showFilenamesList():
    try:
        extensions = ['.jpg','.jpeg','.png']
        chooseWorkdir()
        filenames = filter(os.listdir(workdir), extensions)
        lw_files.clear()
        workimage.clear()
        for filename in filenames:
            lw_files.addItem(filename)  
        Ib_image.setText('Картинка')
    except:
        Ib_image.setText('Вы не выбрали папку')

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            result.append(filename)
    return result

def showChosenImage():
    if lw_files.currentRow() >= 0:
        try:
            filename = lw_files.currentItem().text()
            workimage.loadImage(workdir, filename)
            image_path = os.path.join(workimage.dir, workimage.filename)
            workimage.showImage(image_path)
        except:
            Ib_image.setText('Файл не поддерживается или поврежден')

def saveImage(self):
    path = os.path.join(workdir, self.save_dir)
    if not(os.path.exists(path) or os.path.isdir(path)):
        os.mkdir(path)
    image_path = os.path.join(path, self.filename)
    self.image.save(image_path)

#глобальные переменные
workdir = ''                  

app = QApplication([])

#окно 
win = QWidget()
win.resize(700, 500)

#виджеты
Ib_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()
btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")

#лэйауты
mainLine = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(Ib_image, 95)
buttons = QHBoxLayout()
buttons.addWidget(btn_left)
buttons.addWidget(btn_right)
buttons.addWidget(btn_flip)
buttons.addWidget(btn_sharp)
buttons.addWidget(btn_bw)
col2.addLayout(buttons)

mainLine.addLayout(col1, 20)
mainLine.addLayout(col2, 80)
win.setLayout(mainLine)

workimage = ImageProcessor()

#подписки на события
btn_dir.clicked.connect(showFilenamesList)
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_right.clicked.connect(workimage.do_right)
btn_left.clicked.connect(workimage.do_left)
btn_sharp.clicked.connect(workimage.do_blur)

win.show()
app.exec()