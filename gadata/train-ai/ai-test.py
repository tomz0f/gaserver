from imageai.Detection import ObjectDetection
import os
def testAi():
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath( os.path.join(execution_path , "galari/models/best.pt"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "galari/test/2.jpeg"), output_image_path=os.path.join(execution_path , "galari/test/2.jpeg"), minimum_percentage_probability=30)

    for eachObject in detections:
        return eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"]

if __name__=="__main__":
    testAi()