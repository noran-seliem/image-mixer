
import os, sys
import numpy as np
from PIL import Image
import cv2
from numpy import asarray
import numpy as np
import pyqtgraph as pg
from PIL import Image
from matplotlib import image as im
import scipy
import scipy.fftpack
from scipy import signal
from scipy.fftpack import fft, fftshift
from numpy.fft import fft,fftfreq,ifft





class IMage_model():
    
     def __init__(self, imgPath: str ="test"):
        if imgPath != "test":

            self.imgPath = imgPath
            
            # the following to use it in mix function
           
            self.imgByte = cv2.imread(self.imgPath,0).T
            self.dft = np.fft.fft2(self.imgByte)
            self.real = np.real(self.dft)
            self.imaginary = np.imag(self.dft)
            self.magnitude = abs(self.dft)
            self.phase = np.angle(self.dft)
            print("phase" , self.phase)
            rows,cols=self.magnitude.shape
            self.UnitMagnitude=np.ones((rows,cols))
            rows,cols=self.phase.shape
            self.UnitPhase=np.zeros((rows,cols))
            
        
       
            
            
            
            
            
     def OpenImage(self):
        self.theimage=cv2.imread(self.imgPath,0)
        image = pg.ImageItem(self.theimage)      
        return image

     def FTMag(self):
        theImage=cv2.imread(self.imgPath,0)
        #f = np.fft.fft2(theImage)
        fourier=np.fft.fft2(theImage)
        shifted_FFT = np.fft.fftshift(fourier)
        self.shifted_magnitude = np.log(np.abs(shifted_FFT))
        #self.magnitude = abs(f)
        return self.shifted_magnitude
    
     def FTPhase(self):
        theImage=cv2.imread(self.imgPath,0)
        fourier=np.fft.fft2(theImage)
        phase2=np.angle(fourier)
        return phase2

     def FTReal(self):
        theImage=cv2.imread(self.imgPath,0)
        fourier=np.fft.fft2(theImage)
        shifted_FFT = np.fft.fftshift(fourier)
        self.shifted_real =  20*np.log(np.real(shifted_FFT))
       # self.real=np.real(fourier)
                     
        return self.shifted_real 

     def FTImag(self):
        theImage=cv2.imread(self.imgPath,0)
        fourier=np.fft.fft2(theImage)
        self.fshift = np.fft.fftshift(fourier)
        self.shifted_imag=np.imag(self.fshift)
        #self.shifted_imag[self.shifted_imag<=0]=10**-8
        #self.shifted_imag=20*np.log(self.shifted_imag)
        #self.imaginary=np.imag(fourier)
        return self.shifted_imag

    
        
        
    
     def mix(self, imageToBeMixed, magnitudeOrRealRatio: float,phaseOrImaginaryRatio: float, mode):
         if(mode=='realandimaginary'):
             self.Real_select=magnitudeOrRealRatio*self.real+(1-magnitudeOrRealRatio)*imageToBeMixed.real
             self.imag_select=self.imaginary*(1-phaseOrImaginaryRatio)+imageToBeMixed.imaginary*(phaseOrImaginaryRatio)
             self.fourier_result=self.Real_select+1j*self.imag_select
              
        
         
         elif(mode=='imaginaryandreal'):
             self.Real_select=self.real*(1-magnitudeOrRealRatio)+imageToBeMixed.real*(magnitudeOrRealRatio)
             self.imag_select=self.imaginary*phaseOrImaginaryRatio+(1-phaseOrImaginaryRatio)*imageToBeMixed.imaginary
             self.fourier_result=self.Real_select+1j*self.imag_select
         
        
         elif(mode=='magnitudeandphase'):
             self.Mag_select=self.magnitude*magnitudeOrRealRatio+(1-magnitudeOrRealRatio)*imageToBeMixed.magnitude
             self.Phase_select =self.phase*(1-phaseOrImaginaryRatio)+imageToBeMixed.phase*(phaseOrImaginaryRatio)
            
             self.fourier_result=np.multiply(self.Mag_select,np.exp(1j*self.Phase_select))
             
             self.fourier_result=np.fft.fftshift(self.fourier_result)
            
             
        
          
         elif(mode=='unitmagnitude'):
             self.Mag_select=self.UnitMagnitude*magnitudeOrRealRatio+(1-magnitudeOrRealRatio)*imageToBeMixed.UnitMagnitude
             self.Phase_select=self.phase*(1-phaseOrImaginaryRatio)+imageToBeMixed.phase*(phaseOrImaginaryRatio)
             self.fourier_result=np.multiply(self.Mag_select,np.exp(1j*self.Phase_select))
             print(type(self.fourier_result))
         
         
         elif(mode=='unitphase'):
             self.Mag_select=self.magnitude*magnitudeOrRealRatio+(1-magnitudeOrRealRatio)*imageToBeMixed.magnitude
             self.phase_select=self.UnitPhase*(1-phaseOrImaginaryRatio)+imageToBeMixed.UnitPhase*(phaseOrImaginaryRatio)
             self.fourier_result=np.multiply(self.Mag_select,np.exp(1j*self.Phase_select))
             self.fourier_result=np.multiply(self.Mag_select,np.exp(1j*self.Phase_select))
             print(type(self.fourier_result))
             
         elif(mode=='unitmagandunitphase'):
             self.Mag_select=self.UnitMagnitude*magnitudeOrRealRatio+(1-magnitudeOrRealRatio)*imageToBeMixed.UnitMagnitude
             self.Phase_select=self.UnitPhase*(1-phaseOrImaginaryRatio)+imageToBeMixed.UnitPhase*(phaseOrImaginaryRatio)
             self.fourier_result=np.multiply(self.Mag_select,np.exp(1j*self.Phase_select))
           
             
             
         
         
         print(2)
        
         InverseImage=np.real(np.fft.ifft2(self.fourier_result ))
         InverseImage=np.flip(InverseImage, 1)
         print(InverseImage)
         return (InverseImage)  
      
      
              

     