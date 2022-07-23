import numpy as np

def generate_samples(n):
    samples =[]
    for i in range(n):
        sample = np.cos(2*np.pi/n*3*i)
        samples.append(sample+(0.j))
    return samples