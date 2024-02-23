from ctypes import *

class FaceBox(Structure):
    _fields_ = [("x1", c_int32), ("y1", c_int32), ("x2", c_int32), ("y2", c_int32), 
        ("liveness", c_float), 
        ("yaw", c_float), ("roll", c_float), ("pitch", c_float), 
        ("face_quality", c_float), ("face_luminance", c_float), ("eye_dist", c_float),
        ("left_eye_closed", c_float), ("right_eye_closed", c_float), 
        ("face_occlusion", c_float), ("mouth_opened", c_float), 
        ("landmark_68", c_float * 136)
        ]