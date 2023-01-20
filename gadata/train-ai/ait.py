from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath("idenprof/models/resnet50-idenprof-test_acc_1.00000_epoch-0.pt")
detector.setJsonPath("idenprof/models/idenprof_model_classes.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="3.jpeg", output_image_path="3-detected.jpeg")
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
