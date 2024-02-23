import os

from ctypes import *
from numpy.ctypeslib import ndpointer
from facebox import FaceBox

libPath = os.path.abspath(os.path.dirname(__file__)) + '/libfacesdk1.so'
facesdk = cdll.LoadLibrary(libPath)

getMachineCode = facesdk.getMachineCode
getMachineCode.argtypes = []
getMachineCode.restype = c_char_p

setActivation = facesdk.setActivation
setActivation.argtypes = [c_char_p]
setActivation.restype = c_int32

initSDK = facesdk.initSDK
initSDK.argtypes = [c_char_p]
initSDK.restype = c_int32

faceDetection = facesdk.faceDetection
faceDetection.argtypes = [ndpointer(c_ubyte, flags='C_CONTIGUOUS'), c_int32, c_int32, POINTER(FaceBox), c_int32]
faceDetection.restype = c_int32

