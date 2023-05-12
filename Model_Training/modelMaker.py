import os

import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
assert tf.__version__.startswith('2')
import time
'''
from tflite_model_maker import model_spec
from tflite_model_maker import image_classifier
from tflite_model_maker.config import ExportFormat
from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.image_classifier import DataLoader'''
import DataLoader
import matplotlib.pyplot as plt

image_path = r'C:\TrainingImages'
data = DataLoader.from_folder(image_path)

train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)


def preprocess_image(image_path, input_size):
  """Preprocess the input image to feed to the TFLite model"""
  img = tf.io.read_file(image_path)
  img = tf.io.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.uint8)
  original_image = img
  resized_img = tf.image.resize(img, input_size)
  resized_img = resized_img[tf.newaxis, :]
  return resized_img, original_image


def set_input_tensor(interpreter, image):
  """Set the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Retur the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  # Feed the input image to the model
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all outputs from the model
  scores = get_output_tensor(interpreter, 0)
 #// boxes = get_output_tensor(interpreter, 1)
  #count = int(get_output_tensor(interpreter, 2))
  #classes = get_output_tensor(interpreter, 3)
  print(scores)
  return scores


def run_odt_and_draw_results(image_path, interpreter, threshold=0.5):
  """Run object detection on the input image and draw the detection results"""
  # Load the input shape required by the model
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  # Load the input image and preprocess it
  preprocessed_image, original_image = preprocess_image(
      image_path, 
      (input_height, input_width)
    )

  # Run object detection on the input image
  results = detect_objects(interpreter, preprocessed_image, threshold=threshold)
 
  # Plot the detection results on the input image
  return results

'''
print('Creating')
model = image_classifier.create(train_data, validation_data=validation_data)
print("Summarizing")
model.summary()
print("Evaluating")
loss, accuracy = model.evaluate(test_data)



model.export(export_dir='.')
'''

# assign directory
directory = r'C:\TrainingImages'
# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path=(r'C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\model.tflite'))
interpreter.allocate_tensors()
# iterate over files in
# that directory
correctCount = 0
totalCount = 0
for filename in os.listdir(directory):
    dirs = os.path.join(directory, filename)
    for f in os.listdir(dirs):
        INPUT_IMAGE_URL = dirs+'\\'+f
        # checking if it is a file
        
        if os.path.isfile(INPUT_IMAGE_URL):
            print('--------')
            print(INPUT_IMAGE_URL)
            startTime = time.time()
            DETECTION_THRESHOLD = 0.5 

            

            # Run inference and draw detection result on the local copy of the original file
            result = run_odt_and_draw_results(
                INPUT_IMAGE_URL, 
                interpreter, 
                threshold=DETECTION_THRESHOLD)
            if(result[0] > result[1]):
                print("Leopard")
                if('Leopard' in INPUT_IMAGE_URL):
                    correctCount += 1
            else:
                print("Human")
                if('People' in INPUT_IMAGE_URL):
                    correctCount += 1
            totalCount +=1 
            print(f'{correctCount}/{totalCount} Correct')
            print(f"Took {startTime-time.time()} secs")
            print('--------')

