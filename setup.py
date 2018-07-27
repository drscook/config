############################################################################################################# 
# Super-Importer created by Geir Arne Hjelle.  Will attempt to pip install module if not found by normal import.
############################################################################################################# 
from importlib.abc import MetaPathFinder
from importlib import util
import subprocess
import sys

class PipFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        print(f"Module {self} not installed.  Attempting to pip install")
        cmd = f"{sys.executable} -m pip install {self}"
        try:
            subprocess.run(cmd.split(), check=True)
        except subprocess.CalledProcessError:
            return None
        return util.find_spec(self)

############################################################################################################# 
# Standard modules
############################################################################################################# 
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import itertools as it
import math
import numba as nb



############################################################################################################# 
# Commonly used modules
############################################################################################################# 
def import_numba_cuda():
    def test():
        print("\n")
        result = False
        try:
            import numba as nb
            import numba.cuda as cuda
            A = np.arange(3)
            A_gpu = cuda.to_device(A)
#             A = nb.SmartArray(np.arange(3))
            @cuda.jit
            def double_gpu(A):
                tx = cuda.threadIdx.x
                A[tx] = 2*A[tx]
            double_gpu[1,3](A_gpu)
            A *= 2
            result = np.allclose(A, A_gpu.copy_to_host())
        except:
            pass
        return result

    result = test()
    if result == True:
        print("Cuda.jit is installed and working!")        
    else:
        print("Cuda.jit not working yet.  Trying to conda install.")
        try:
            os.system('conda update conda')
            os.system('conda install -c numba cudatoolkit')
            os.system('conda install -c numba numba')
            result = test()
        except:
            pass
        if result == True:
            print("That worked!! Cuda.jit is installed and working!")
        else:
            print("That failed.  Cuda.jit not working yet.  Trying to pip install.")
            try:
                os.system('apt-get update')
                os.system('apt install -y --no-install-recommends -q nvidia-cuda-toolkit')
                os.system('pip install --upgrade numba')
                os.system('apt-get update')
                os.environ['NUMBAPRO_LIBDEVICE'] = "/usr/lib/nvidia-cuda-toolkit/libdevice"
                os.environ['NUMBAPRO_NVVM'] = "/usr/lib/x86_64-linux-gnu/libnvvm.so"
                result = test()
            except:
                pass
            if result == True:
                print("That worked!! Cuda.jit is installed and working!")
            else:
                print("That failed too.  I give up.")
    return result




############################################################################################################# 
# Preferences
############################################################################################################# 
np.set_printoptions(precision=4, suppress=True)





############################################################################################################# 
# Utility functions
############################################################################################################# 
def listify(X):
    """
    Ensure X is a list
    """
    if isinstance(X, list):
        return X
    elif (X is None) or (X is np.nan):
        return []
    elif isinstance(X,str):
        return [X]
    else:
        try:
            return list(X)
        except:
            return [X]
        
        
def cross_subtract(u,v=None):
    if v is None:
        v=u.copy()
    with np.errstate(invalid='ignore'):  # suppresses warnings for inf-inf
        w = u[:,np.newaxis] - v[np.newaxis,:]
        w[np.isnan(w)] = np.inf
    return w


def wedge(a,b):
    """
    Geometric wedge product
    """
    return np.outer(b,a)-np.outer(a,b)


def contract(A, keepdims=[0]):
    """
    Sum all dimensions except those in keepdims
    """
    keepdims = listify(keepdims)
    A = np.asarray(A)
    return np.einsum(A, range(A.ndim), keepdims)


def make_unit(A, axis=-1):
    """
    Normalizes along given axis so the sum of squares is 1
    """
    A = np.asarray(A)
    M = np.linalg.norm(A, axis=axis, keepdims=True)
    return A / M


def make_symmetric(A, skew=False):
    """
    Returns symmetric or skew-symmatric matrix by copying upper triangular onto lower.
    """
    A = np.asarray(A)
    U = np.triu(A,1)
    if skew == True:
        return U - U.T
    else:
        return np.triu(A,0) + U.T    

