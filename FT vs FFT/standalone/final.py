import ctypes
from ctypes import *
import time
from os import path
import numpy as np
from matplotlib import pyplot as plot

THIS_FOLDER= path.dirname(path.abspath(__file__))
My_Library = CDLL(path.join(THIS_FOLDER, "lib.so"))

N=[8,16,32,64,128,256,1024,2048]
FFT=[]
DFT=[]
error=[]
Time_FFT=[]
Time_DFT=[]


class CComplex(ctypes.Structure):
    # Complex number, compatible with std::complex layout
    _fields_ = [("real", ctypes.c_double), ("imag", ctypes.c_double)]

    def __init__(self, pycomplex):
        # Init from Python complex
        self.real = pycomplex.real
        self.imag = pycomplex.imag

    def to_complex(self):
        # Convert to Python complex
        return self.real + (1.j) * self.imag


def discret_fourier (sample):

    sample_c = (CComplex * len(sample))(*(CComplex(r) for r in sample))

    output_c=(CComplex * len(sample))()

    start = time.perf_counter()
    My_Library.discret_fourier(output_c,len(sample),sample_c)
    end = time.perf_counter()

    time_dft=((end) - (start))*1000

    result=[]
    for i in range (len(output_c)):
        result.append(output_c[i].to_complex())

    return(result,time_dft)



def fast_fourier (sample):
    sample_c = (CComplex * len(sample))(*(CComplex(r) for r in sample))

    start = time.perf_counter()
    My_Library.f_fourier(sample_c,len(sample))
    end = time.perf_counter()
    time_fft=((end) - (start))*1000

    result=[]
    for i in range (len(sample_c)):
        result.append(sample_c[i].to_complex())

    return(result,time_fft)




def generate_signal(n):
    samples =[]
    for i in range(n):
        sample = np.cos(2*np.pi/n*3*i)
        samples.append(sample+(0.j))
    return samples




def Error (dft_array,fft_array):
    rms=np.square(np.subtract(dft_array,fft_array)).mean()
    return rms


for n in N:

   sample=generate_signal(n)
   fft,time_fft=fast_fourier(sample)
   dft,time_dft=discret_fourier(sample)

   err=Error(dft,fft)

   Time_FFT.append(time_fft)
   Time_DFT.append(time_dft)

   FFT.append(fft)
   DFT.append(dft)
   error.append(err)

   error_abs=np.abs(error)



########### ERROR PLOT  (error with number of samples) ###########

# plot.plot(N,error_abs,label="error")
# plot.xlabel("Samples(N)")
# plot.ylabel("Error")
# plot.legend()
# plot.tight_layout

# plot.show()


###### PLOT FT and FFT (time with number of samples) #####

# plot.plot(N,Time_DFT,'r',label='FT')
# plot.plot(N,Time_FFT,'b',label='FFT')
# plot.legend()
# plot.xlabel("Samples(N)")
# plot.ylabel("Time (ms)")
# plot.show()


########### plot style 1 ERROR plus plot of FT and FFT ###########

plot.subplot(2, 1, 1)
plot.plot(N,Time_DFT,'r',label='DFT')
plot.plot(N,Time_FFT,'b',label='FFT')
plot.legend()
plot.xlabel("Samples(N)")
plot.ylabel("Time (ms)")

plot.subplot(2, 1, 2)
plot.plot(N,error_abs,label="error")
plot.xlabel("Samples(N)")
plot.ylabel("Error")
plot.legend()

plot.tight_layout()

plot.show()



