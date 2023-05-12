import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

# Visualization parameters
_ROW_SIZE = 20  # pixels
_LEFT_MARGIN = 24  # pixels
_TEXT_COLOR = (0, 0, 255)  # red
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_FPS_AVERAGE_FRAME_COUNT = 10


def run(model: str, max_results: int, score_threshold: float, num_threads: int, enable_edgetpu: bool, camera_id: int, width: int, height: int) -> None:


  # Initialize the image classification model
  base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)

  # Enable Coral by this setting
  classification_options = processor.ClassificationOptions(max_results=max_results, score_threshold=score_threshold)
  options = vision.ImageClassifierOptions(base_options=base_options, classification_options=classification_options)

  classifier = vision.ImageClassifier.create_from_options(options)

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create TensorImage from the RGB image
    tensor_image = vision.TensorImage.create_from_array(rgb_image)
    # List classification results
    categories = classifier.classify(tensor_image)
    print(categories)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break
    cv2.imshow('image_classification', image)

  cap.release()
  cv2.destroyAllWindows()


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Name of image classification model.',
      required=False,
      default='efficientnet_lite0.tflite')
  parser.add_argument(
      '--maxResults',
      help='Max of classification results.',
      required=False,
      default=3)
  parser.add_argument(
      '--scoreThreshold',
      help='The score threshold of classification results.',
      required=False,
      type=float,
      default=0.0)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      default=4)
  parser.add_argument(
      '--enableEdgeTPU',
      help='Whether to run the model on EdgeTPU.',
      action='store_true',
      required=False,
      default=False)
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      default=480)
  args = parser.parse_args()

  run(args.model, int(args.maxResults),
      args.scoreThreshold, int(args.numThreads), bool(args.enableEdgeTPU),
      int(args.cameraId), args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()