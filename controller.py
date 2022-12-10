import ffmpeg
from PyQt6 import *

import subprocess
from ui import *
import shutil
import os

class Controller(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__JXL = False
        self.__trans = True
        self.__modelpath = ""
        self.__inputpath = ""
        self.__imagefolder = ""
        #self.progressBar.setProperty("value", 0)
        self.setupUi(self)
        # Following is no longer needed as of QT6
        #self.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        #self.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

        self.buttonBox.accepted.connect(lambda: self.submit())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(lambda: self.clear())
        self.buttonBox.rejected.connect(lambda: self.kill())
        self.pushButton.clicked.connect(lambda: self.BrowseModel())
        self.pushButton_2.clicked.connect(lambda: self.BrowseInput())
        self.radioButton.clicked.connect(lambda: self.setPNG())
        self.radioButton_2.clicked.connect(lambda: self.setJXL())
        self.checkBox.clicked.connect(lambda: self.setTrans())
        # remove the graphicsView elements until I figure out how they work
        self.graphicsView.close()
        self.graphicsView_2.close()

    def submit(self):
        if self.__modelpath == "":
            print("path needed")
        elif self.__modelpath == "":
            print("path needed")
        else:
            #shutil.rmtree('outputTemp')
            #shutil.rmtree('inputTemp')
            #progress bar throws error, maybe due to threading stuff QT does?
            #self.progressBar.setValue("0")
            os.makedirs('inputTemp')
            os.makedirs('outputTemp')
            if self.__trans == True:
                inputvars = f"-i ../inputTemp -o ../outputTemp -am bg_difference {self.__modelpath}"
            else:
                inputvars = f"-i ../inputTemp -o ../outputTemp {self.__modelpath}"
            outputpath = os.path.abspath(self.__inputpath)
            #filenamenoext = os.path.splitext(self.__inputpath)[0]
            filename = os.path.basename(self.__inputpath).split('/')[-1]
            shutil.copyfile(self.__inputpath, f"./inputTemp/upscaled_{filename}")
            subprocess.run(f"python upscale.py {inputvars}", shell=True, cwd="./ESRGAN")
            #self.progressBar.setValue("50")
            if self.__JXL == True:
                subprocess.run(f"ffmpeg -i ./outputTemp/upscaled_{filename} -c:v libjxl {self.__inputpath}_{os.path.basename(self.__modelpath).split('/')[-1]}.jxl")
                #figure out setting up image previews with QT
                #self.graphicsView_2.setObjectName()
            else:
                shutil.copyfile(f"./outputTemp/upscaled_{filename}", f"{self.__inputpath}_{os.path.basename(self.__modelpath).split('/')[-1]}.png")
            #self.progressBar.setValue("75")
            shutil.rmtree('outputTemp')
            shutil.rmtree('inputTemp')
            #self.progressBar.setValue("100")

    def clear(self):
        self.__JXL = False
        self.__trans = True
        self.__modelpath = ""
        self.__inputpath = ""
        self.__imagefolder = ""
        self.checkBox.setChecked(True)
        self.radioButton.setChecked(True)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.graphicsView.close()
        self.graphicsView_2.close()

    def kill(self):
        self.close()

    def setPNG(self):
        self.__JXL = False

    def setJXL(self):
        self.__JXL = True

    def setTrans(self):
        self.__trans = self.checkBox.isChecked()

    def BrowseModel(self):
        self.__modelpath = QtWidgets.QFileDialog.getOpenFileName(None, 'Select .pth File', "", "ESRGAN Model Files (*.pth)")[0]
        self.lineEdit.setText(self.__modelpath)
        self.lineEdit_2.setText(os.path.basename(self.__modelpath).split('/')[-1])
        print(self.__modelpath)

    def BrowseInput(self):
        self.__inputpath = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image File', "", "Image Files (*.png)")[0]
        self.lineEdit_3.setText(os.path.basename(self.__inputpath).split('/')[-1])
        self.lineEdit_4.setText(self.__inputpath)
        print(self.__inputpath)
