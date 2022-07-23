from matplotlib import pyplot as plot
import c_complex
from fourier import *
from generate_signal import generate_samples

N=[8,16,32,64,128,256,1024]
FFT=[]
FT=[]
error=[]
Time_FFT=[]
Time_DFT=[]


for n in N:

   sample=generate_samples(n)

   fft,time_fft=fast_fourier(sample)
   dft,time_dft=discret_fourier(sample)

   e=Error(dft,fft)
   
   Time_FFT.append(time_fft)
   Time_DFT.append(time_dft)
   
   FFT.append(fft)
   FT.append(dft)
   error.append(e)

   error_abs=np.abs(error)





########### ERROR PLOT  (error with number of samples) ###########

# plot.plot(N,error_abs,label="error")
# plot.xlabel("Samples(N)")
# plot.ylabel("Error")
# plot.legend()
# plot.tight_layout

# plot.show()


###### PLOT FT and FFT (time with number of samples) #####

# plot.plot(N,Time_DFT,'r',label='DFT')
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








