import imutils
import numpy as np
import cv2

def detect_faces(image_path):
  """Detects faces in an image using a pre-trained model.

  Args:
    image_path: Path to the image file.

  Returns:
    The image with bounding boxes drawn around detected faces.
  """

  # Load the pre-trained face detection model
  prototxt = 'deploy.prototxt'  # Assuming these files are in the same directory
  model = 'res10_300x300_ssd_iter_140000.caffemodel'
  net = cv2.dnn.readNetFromCaffe(prototxt, model)

  # Read and resize the image
  image = cv2.imread(image_path)
  image = imutils.resize(image, width=400)
  (h, w) = image.shape[:2]

  # Create a blob from the image
  blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

  # Pass the blob through the network
  net.setInput(blob)
  detections = net.forward()

  # Loop over the detections and draw boxes around faces
  for i in range(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      (startX, startY, endX, endY) = box.astype("int")
      text = "{:.2f}%".format(confidence * 100)
      y = startY - 10 if startY - 10 > 10 else startY + 10
      cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
      cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

  return image

if __name__ == "__main__":
  # Replace 'path/to/your/image.jpg' with the actual path to your image
  image_with_faces = detect_faces('path/to/your/image.jpg')

  # Display the image with detected faces (you might need to use a different method for displaying images in your local environment)
  cv2.imshow("Faces Detected", image_with_faces)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

