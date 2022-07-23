import ctypes
from ctypes import *


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