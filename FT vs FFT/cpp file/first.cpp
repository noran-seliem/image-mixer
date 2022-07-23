#include<iostream>
#include<math.h>
using namespace std;
#define PI 3.14159265
#include<complex>
int n =16;
#include <chrono>
 

extern "C" 
{
   void discret_fourier(complex<double> *output,int N,complex<double> *sample);
   void f_fourier(std::complex<double> *sample,int N);
    } 

void discret_fourier(complex<double> *output,int N,complex<double> *sample)
{   //temprory variables 
    complex<double> temp;
    //dft function



    for (int k=0; k<N; k++)
    {
        temp= (0,0);

        for (int n=0; n<N; n++)
        {
            double real= cos(((2*M_PI)/N)*k*n);
            double img= sin(((2*M_PI)/N)*k*n);
            complex<double> cmplx (real, -img);
            temp+= sample[n]*cmplx;
            
        }
        output[k]=temp;
        
        
        
    }
    
}

  void f_fourier(std::complex<double> *sample,int N)//o(nlog(n)
    {   	
        if (N <= 1) {return;}
        std::complex<double> odd_sample[N/2];
    	std::complex<double> even_sample[N/2];
    	for (int i = 0; i < N / 2; i++) 
    	    {
    		    even_sample[i] = sample[i*2];
        		odd_sample[i] = sample[i*2+1];
        	}
    
    	f_fourier(even_sample, N/2);
    	f_fourier(odd_sample, N/2);
        
        
        for (int k = 0; k < N / 2.0; k++)
    	    {
        		std::complex<double> temp = exp(std::complex<double>(0, -2 * M_PI * k / N)) * odd_sample[k];
        		sample[k] = even_sample[k] + temp;
        		sample[N / 2 + k] = even_sample[k] - temp;
                
              


            }
            

    }       
