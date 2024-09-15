# Face Detection Using OpenCV and Colab

This script is designed to capture an image using a webcam, detect faces within the image, and display the image with bounding boxes drawn around any detected faces. It leverages OpenCV's deep learning face detection capabilities and integrates with Google Colab for easy use in a browser-based environment.

## Overview

### Key Steps:
1. **Capture a photo** from your webcam using a JavaScript interface within Google Colab.
2. **Download a pre-trained face detection model** (Caffe model) from the OpenCV repository.
3. **Process the captured image** by resizing it and preparing it for face detection.
4. **Detect faces** in the image using OpenCV's deep learning-based face detection.
5. **Draw bounding boxes** around the detected faces with the confidence percentage displayed.
6. **Show the processed image** with the detected faces highlighted.

### Libraries and Tools Used:
- **OpenCV**: Used for image manipulation, face detection, and displaying the results.
- **imutils**: Helps simplify image resizing.
- **Google Colab Patches**: Used for displaying images and interacting with the webcam in Colab.
- **JavaScript**: Provides an interface for capturing the webcam photo within the Colab environment.

---

## Code Breakdown

### 1. **Take a Photo Using the Webcam**

The `take_photo()` function captures an image from your webcam. It uses JavaScript to access the webcam, display a "Capture" button, and return the captured image.

```python
from google.colab.patches import cv2_imshow
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
  ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename
