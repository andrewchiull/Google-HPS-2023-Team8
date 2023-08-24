# [How to implement gesture\_recognizer.task for Live stream · Issue #4448 · google/mediapipe](https://github.com/google/mediapipe/issues/4448)
# https://github.com/google/mediapipe/issues/4448#issuecomment-1562674509

import mediapipe as mp
import cv2
import numpy as np

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)

class Result():
    H, W = 1, 1
    img = np.ndarray((H, W, 3), np.uint8) # empty image
    gestures = list()
res = Result()

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # TODO imshow
    res.img = output_image.numpy_view()
    res.gestures = result.gestures
    print(result.gestures)



options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='/Users/andrewchiu/Google-HPS-2023-Team8/src/cv/mp/gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

timestamp = 0

with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)

        cv2.imshow('Show', res.img)
        print("outside", res.gestures)
        

        if cv2.waitKey(5) & 0xFF == 27:
            break

video.release()
cv2.destroyAllWindows()