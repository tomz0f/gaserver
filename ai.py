#!/bin/python3
# Load TensorFlow Lite and trained model
from sklearn.metrics import accuracy_score
import tensorflow as tf

test_images = 'gadata'
interpreter = tf.lite.Interpreter(model_path="galarisi3.tflite")
interpreter.allocate_tensors()

input_tensor_index = interpreter.get_input_details()[0]["index"]
output_tensor_index = interpreter.get_output_details()[0]["index"]

# Preprocess test images
test_images = [preprocess_image(image) for image in test_images]
test_images = np.vstack(test_images)

# Run model on test images
interpreter.set_tensor(input_tensor_index, test_images)
interpreter.invoke()
predictions = interpreter.get_tensor(output_tensor_index)

# Evaluate model performance

accuracy = accuracy_score(test_labels, predictions)
print(f"Model accuracy: {accuracy:.2f}")

#!/usr/bin/python3
#test codes
from imageai.Classification.Custom import CustomImageClassification
import os

execution_path = os.getcwd()

prediction = CustomImageClassification()
prediction.setModelTypeAsResNet50()
prediction.setModelPath("idenprof_061-0.7933.h5")
prediction.setJsonPath("idenprof_model_class.json")
prediction.loadModel(num_objects=10)

predictions, probabilities = prediction.predictImage("image.jpg", result_count=3)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)
