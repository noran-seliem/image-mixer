from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMainWindow
import os
from os import path
import cv2
import numpy as np
from PyQt5.QtWidgets import QMessageBox
import logging
import matplotlib.pyplot as plt
from matplotlib import image as im
from mixer import  IMage_model
from PIL import Image
import pyqtgraph as pg
from numpy import asarray







THIS_FOLDER= path.dirname(path.abspath(__file__))
FORM_CLASS,_=loadUiType(path.join(THIS_FOLDER, "fourier.ui"))



 
logging.basicConfig(filename='LogFile.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
#self.logger = logging.getLogger()
#self.logger.setLevel(logging.DEBUG)
 



class MainApp(QtWidgets.QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
       
        
        
   
        
       
    
    
    
    def handle_UI(self):
        _translate = QtCore.QCoreApplication.translate
        
        
        
        
        
        
        
        self.original_1.getPlotItem().hideAxis('bottom')
        self.original_1.getPlotItem().hideAxis('left')
        self.component2.getPlotItem().hideAxis('bottom')
        self.component2.getPlotItem().hideAxis('left')
        self.original_2.getPlotItem().hideAxis('bottom')
        self.original_2.getPlotItem().hideAxis('left')
        self.component1.getPlotItem().hideAxis('bottom')
        self.component1.getPlotItem().hideAxis('left')
        self.output1.getPlotItem().hideAxis('bottom')
        self.output1.getPlotItem().hideAxis('left')
        self.output2.getPlotItem().hideAxis('bottom')
        self.output2.getPlotItem().hideAxis('left')
        
        
        #######################events#####################
        
        self.image1.clicked.connect(self.Image_UPload)
        self.image2.clicked.connect(self.Image_UPload)
      
        self.components1.activated.connect(lambda:self.selected_components())
        self.components2.activated.connect(lambda:self.selected_components())
        #self.components1.activated.connect(lambda:self.FOURIERPhase())
        #self.components2.activated.connect(lambda:self.FOURIERPhase())
        #self.components1.activated.connect(lambda:self.FOURIERReal())
        #self.components2.activated.connect(lambda:self.FOURIERReal())
        #self.components1.activated.connect(lambda:self.FOURIERImaginary())
        #self.components2.activated.connect(lambda:self.FOURIERImaginary())
        self.mixcomp2.clear()
        self.imgcom1.activated.connect(lambda:self.select_ImageIncomponent1())
        self.imgcom2.activated.connect(lambda:self.select_ImageIncomponent2())
        self.mixcomp1.activated.connect(lambda:self.select_FourierIncomponent1())
        self.mixcomp2.activated.connect(lambda:self.select_FourierIncomponent2())
        
        
        
        
        self.outselect.activated.connect(lambda:self.mix_function())
      
    
        
        
        
        
        
        
        
        
        
        
                                     ##########load_images########
        
        
    def Image_UPload(self):
        self.senderobject = self.sender()
     
        repo_path = "C:/Users/Start/Documents/fft/third.task/images"
        filePaths = QtWidgets.QFileDialog.getOpenFileNames(self, 'load image',repo_path, "*.jpg;;" "*.jpeg;;" "*.png;;" )   
        for filePath in filePaths:
            for self.f in filePath:
                if self.f == '*':
                     break
                if (self.senderobject.text()=='image1'):               
                    self.Imagemodel1=IMage_model(self.f)
        
                    self.image1=self.Imagemodel1.OpenImage()
                    
                    # gettin the size of first image
                    self.a=Image.open(self.f)
                    self.width,self.hight=self.a.size

                    self.original_1.clear()
                    self.original_1.addItem(self.image1)
                    self.image1.rotate(270)
                    logging.info('User chooses Image 1 and showed successfully')

                if(self.senderobject.text()=='image2'):                    
                    self.Imagemodel2=IMage_model(self.f)
                    
                    self.image2=self.Imagemodel2.OpenImage()
                    #size of second image 
                    self.b=Image.open(self.f)
                    width,hight=self.b.size
                    
                    if(self.b.size==self.a.size):
                        self.original_2.clear()
                        self.original_2.addItem(self.image2)
                        self.image2.rotate(270)
                        logging.info('User chooses Image  and showed successfully')
                        logging.info('they are of the same size')
                    else:
                         message=QtWidgets.QMessageBox()
                         logging.info('they are not of the same size')
                         message.setIcon(QtWidgets.QMessageBox.Critical)
                         message.setText("Error! Second Image is not the same size as the first one")
                         message.setInformativeText("Dont Panic :) pick 2 images of the same size and try again later")
                         message.setWindowTitle(" Error message")
                         message.exec_()
                         
                         #########images_components############3
                         
                         
    def selected_components(self):                       
   # def FOURIERTMag(self):
        senderOBJ1 = self.sender()
        if (senderOBJ1.currentText()=='FTMag1'):
            self.component1.clear()
            self.FourierMagImage1=self.Imagemodel1.FTMag()  
            self.magnitude_spectrum1=20*np.log(self.FourierMagImage1)
            print(self.magnitude_spectrum1,'1')
            img1 = pg.ImageItem(asarray(self.magnitude_spectrum1))
            print(img1,'2')
            logging.info('User chooses magnitude of first image')

            self.component1.addItem(img1)
            img1.rotate(270)
        if (senderOBJ1.currentText()=='FTMag2'):
            self.component2.clear()
            self.FourierMagImage2=self.Imagemodel2.FTMag()
            self.magnitude_spectrum2=20*np.log(self.FourierMagImage2)
            img2 = pg.ImageItem(asarray(self.magnitude_spectrum2))
            logging.info('User chooses magnitude of second image')

            self.component2.addItem(img2)
            img2.rotate(270)
                
    
        
        
       
    #def FOURIERPhase(self):
        
        senderOBJ2 = self.sender()
        if(senderOBJ2.currentText()=='FTPhase1'):
            self.component1.clear()
            self.FourierPhaseImage1=self.Imagemodel1.FTPhase()
            PhaseImage1Array = pg.ImageItem(asarray(self.FourierPhaseImage1))
            logging.info('User chooses phase of first image')
            self.component1.addItem(PhaseImage1Array)
            PhaseImage1Array.rotate(270)
        if(senderOBJ2. currentText()=='FTPhase2'):
            self.component2.clear()
            self.FourierPhaseImage2=self.Imagemodel2.FTPhase()
            PhaseImage1Array = pg.ImageItem(asarray( self.FourierPhaseImage2))
            logging.info('User chooses phase of second image')
            self.component2.addItem(PhaseImage1Array)
            PhaseImage1Array.rotate(270)
            

   # def FOURIERReal(self):
        senderOBJ3=self.sender()
        if(senderOBJ3. currentText()=='FTReal1'):
            self.component1.clear()
            self.FourierRealImage1=self.Imagemodel1.FTReal()
            PhaseImage1Array = pg.ImageItem(asarray(self.FourierRealImage1))
            logging.info('User chooses real of first image')
            self.component1.addItem(PhaseImage1Array)
            PhaseImage1Array.rotate(270)
        if(senderOBJ3. currentText()=='FTReal2'):
            self.component2.clear()
            self.FourierRealImage2=self.Imagemodel2.FTReal()
            PhaseImage1Array = pg.ImageItem(asarray(self.FourierRealImage2))
            logging.info('User chooses real of second image')
            self.component2.addItem(PhaseImage1Array)
            PhaseImage1Array.rotate(270)

   # def FOURIERImaginary(self):
        senderOBJ4=self.sender()
        if(senderOBJ4.currentText()=='FTImag1'):
            self.component1.clear()
            self.FourierImaginaryImage1=self.Imagemodel1.FTImag()
            PhaseImage1Array = pg.ImageItem(asarray(self.FourierImaginaryImage1))
            logging.info('User chooses fourier of first image')
            self.component1.addItem(PhaseImage1Array)
            PhaseImage1Array.rotate(270)
        if(senderOBJ4.currentText()=='FTImag2'):
            self.component2.clear()
            self.FourierImaginaryImage2=self.Imagemodel2.FTImag()
            logging.info('User chooses fourier of second image')
            PhaseImage1Array = pg.ImageItem(asarray(self.FourierImaginaryImage2))
            self.component2.addItem(PhaseImage1Array)
            PhaseImage1Array.rotate(270)
            
            
                       ###############mixer####################

    def select_ImageIncomponent1(self):
        senderObject1=self.sender()
        if(senderObject1.currentText()=='img1_c1'):
            logging.info('User chooses image1 in the first component')
            self.whichImage1=self.Imagemodel1
        if(senderObject1.currentText()=='img2_c1'):
            logging.info('User chooses image2 in the first component')
            self.whichImage1=self.Imagemodel2
        return self.whichImage1    
        
        
    

    def select_ImageIncomponent2(self):
        senderObject2=self.sender()
        if(senderObject2.currentText()=='img1_c2'):
            logging.info('User chooses image1 in the second component')
            self.whichImage2=self.Imagemodel1
        if(senderObject2.currentText()=='img2_c2'):
            logging.info('User chooses image2 in the second component')
            self.whichImage2=self.Imagemodel2
        return self.whichImage2    
        
    
    
    
    def select_FourierIncomponent1(self):
        self.senderObject_C1_fourier=self.sender()
        self.senderObject_C1_fourier=str(self.senderObject_C1_fourier.currentText())
        self.mixcomp2.clear()
        if self.mixcomp1.currentText()=="c1Mag" or self.mixcomp1.currentText()=="c1Phase"or self.mixcomp1.currentText()=="c1UnitMag" or self.mixcomp1.currentText()=="c1UnitPhase" :
            self.mixcomp2.addItem("c2Mag");
            self.mixcomp2.addItem("c2Phase");
            self.mixcomp2.addItem("c2UnitMag");
            self.mixcomp2.addItem("c2UnitPhase");
            
        if self.mixcomp1.currentText()=="c1Real" or self.mixcomp1.currentText()=="c1Imag" :
            self.mixcomp2.addItem("c2Real");
            self.mixcomp2.addItem("c2Imag");
    
       

    def select_FourierIncomponent2(self):
        self.senderObject_C2_fourier=self.sender()
        self.senderObject_C2_fourier=str(self.senderObject_C2_fourier.currentText())

    
    def mix_function(self):
        
        
        self.IMGC1=self.select_ImageIncomponent1()
        self.IMGC2=self.select_ImageIncomponent2()
        Imagemodel3= IMage_model()
        self.Slider1Value=int(self.S1Label.text())/100
        self.Slider2Value=int(self.S2Label.text())/100

        
        
        
        #######slider_values_conditions########
        
        if(self.senderObject_C1_fourier=='c1Mag'or self.senderObject_C1_fourier=='c1Real'or self.senderObject_C1_fourier=='c1Unitmag'):
                self.Ratio1=self.Slider1Value
        if (self.senderObject_C1_fourier=='c1Phase' or self.senderObject_C1_fourier=='c1Imag'or self.senderObject_C1_fourier=='c1Unitphase'):
                self.Ratio2=self.Slider1Value
        if (self.senderObject_C2_fourier=='c2Mag'or self.senderObject_C2_fourier=='c2Real'or self.senderObject_C2_fourier=='c2Unitmag'):
                self.Ratio1=self.Slider2Value
        if (self.senderObject_C2_fourier=='c2Phase'or self.senderObject_C2_fourier=='c2Imag'or self.senderObject_C2_fourier=='c2Unitphase'):
                self.Ratio2=self.Slider2Value
                
       ####### mixing magntuide and phase #########
       
       
        if(self.senderObject_C1_fourier=='c1Mag'and self.senderObject_C2_fourier=='c2Phase'):
            self.mode='magnitudeandphase'
            logging.info('User chooses mixing magnitude of first component with phase of second component')
            self.InverseFourier=self.IMGC1.mix(self.IMGC2,self.Ratio1,self.Ratio2, self.mode)
        if(self.senderObject_C2_fourier=='c2Mag'and self.senderObject_C1_fourier=='c1Phase'):
            self.mode='magnitudeandphase'
            logging.info('User chooses mixing magnitude of first second with phase of second first')
            self.InverseFourier=self.IMGC2.mix(self.IMGC1,self.Ratio1,self.Ratio2, self.mode)
            
       
            
        ####### mixing real and imaginary #########
        
        if(self.senderObject_C1_fourier=='c1Imag'and self.senderObject_C2_fourier=='c2Real'):
            self.mode='imaginaryandreal'
            logging.info('User chooses mixing imaginary of first component with real of second component')
            self.InverseFourier=self.IMGC2.mix(self.IMGC1,self.Ratio1,self.Ratio2, self.mode)
            
        if( self.senderObject_C2_fourier=='c2Imag' and self.senderObject_C1_fourier=='c1Real'):
            self.mode='realandimaginary'
            print(1)
            logging.info('User chooses mixing imaginary of second component with real of first component')
            self.InverseFourier=self.IMGC1.mix(self.IMGC2,self.Ratio1, self.Ratio2 , self.mode)
            
            
            #unitmag
            
        if (self.senderObject_C1_fourier=='c1UnitMag' and self.senderObject_C2_fourier=='c2Phase'):
            self.mode='unitmagnitude'
            logging.info('User chooses mixing unitmag of first component with phase of second component')
            self.InverseFourier=self.IMGC1.mix(self.IMGC2,self.Ratio1 , self.Ratio2 , self.mode)
            
        if (self.senderObject_C1_fourier=='c1Phase' and self.senderObject_C2_fourier=='c2UnitMag'):
            self.mode='unitmagnitude'
            logging.info('User chooses mixing unitmag of first component with phase of second component')
            self.InverseFourier=self.IMGC2.mix(self.IMGC1,self.Ratio1 , self.Ratio2 , self.mode)
            
            
            
            #unitphase
            
        if (self.senderObject_C1_fourier=='c1UnitPhase' and self.senderObject_C2_fourier=='c2Mag'):
            self.mode='unitmagnitude'
            logging.info('User chooses mixing unitmag of first component with phase of second component')
            self.InverseFourier=self.IMGC2.mix(self.IMGC1,self.Ratio1 , self.Ratio2 , self.mode)
            
        if (self.senderObject_C1_fourier=='c1Mag' and self.senderObject_C2_fourier=='c2UnitPhase'):
            self.mode='unitmagnitude'
            logging.info('User chooses mixing unitmag of first component with phase of second component')
            self.InverseFourier=self.IMGC1.mix(self.IMGC2,self.Ratio1 , self.Ratio2 , self.mode)
            
            #unitmag and unitphase
            
        if (self.senderObject_C1_fourier=='c1UnitPhase' and self.senderObject_C2_fourier=='c2UnitMag'):
            self.mode='unitmagandunitphase'
           
            self.InverseFourier=self.IMGC2.mix(self.IMGC1, self.Ratio1 , self.Ratio2 , self.mode)
            
        if (self.senderObject_C1_fourier=='c1UnitMag' and self.senderObject_C2_fourier=='c2UnitPhase'):
            self.mode='unitmagandunitphase'
            
            self.InverseFourier=self.IMGC1.mix(self.IMGC2, self.Ratio1 , self.Ratio2 , self.mode)   
            
            
            
            
            
            
            
            
         
            
            
            
        
            
        
        self.InverseFourierArray = pg.ImageItem(asarray(self.InverseFourier))
        self.whichoutput=self.sender()
        if(self.whichoutput.currentText().lower()=='output1'):
            logging.info('user chooses to display result at output1')
            self.output1.clear()
            self.output1.addItem(self.InverseFourierArray)
            print(1)
        if(self.whichoutput.currentText()=='output2'):
            logging.info('user chooses to display result at output2')
            self.output2.clear()
            self.output2.addItem(self.InverseFourierArray)     
       # self.InverseFourierArray.rotate(270)
            
            
     













        
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window= MainApp()
    window.show()  
    app.exec_()
    


if __name__ == '__main__':
    main()