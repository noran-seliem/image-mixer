from os import path
import numpy as np
from c_complex import *
import time

THIS_FOLDER= path.dirname(path.abspath(__file__))
My_Library = CDLL(path.join(THIS_FOLDER, "lib.so"))

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



def Error (dft_array,fft_array):
    rms=np.square(np.subtract(dft_array,fft_array)).mean()
    return rms