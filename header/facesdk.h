#pragma once

#ifdef __cplusplus
extern "C" {
#endif

enum SDK_ERROR
{
	SDK_SUCCESS = 0,
	SDK_LICENSE_KEY_ERROR = -1,
	SDK_LICENSE_APPID_ERROR = -2,
	SDK_LICENSE_EXPIRED = -3,
	SDK_NO_ACTIVATED = -4,
	SDK_INIT_ERROR = -5,
};

typedef struct _tagFaceBox
{
	int x1, y1, x2, y2;	
	float liveness;
	float yaw, roll, pitch;
	float face_quality, face_luminance, eye_dist;
	float left_eye_closed, right_eye_closed, face_occlusion, mouth_opened;
	float landmark_68[68 * 2];
} FaceBox;

/*
* Get the machine code for SDK activation
*/
const char* getMachineCode();

/*
* Activate the SDK using the provided license
*/

int setActivation(char* license);

/*
* Initialize the SDK with the specified model path
*/
int initSDK(char* modelPath);

/*
* Detect faces, perform liveness detection, determine face orientation (yaw, roll, pitch),
* 	assess face quality, detect facial occlusion, eye closure, mouth opening, and identify facial landmarks.
*/
int faceDetection(unsigned char* rgbData, int width, int height, FaceBox* faceBoxes, int faceBoxCount);

#ifdef __cplusplus
}
#endif