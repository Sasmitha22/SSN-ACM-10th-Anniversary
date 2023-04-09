import cv2
import numpy as np
import pyttsx3

# Load YOLOv3 weights and configuration file
cfg = r"C:\Users\Admin\Desktop\IFP - Mine\yolov3.cfg"
weight = r"C:\Users\Admin\Desktop\IFP - Mine\yolov3.weights"
net = cv2.dnn.readNetFromDarknet(cfg, weight)
#net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load list of classes
classes = []
with open(r"C:\Users\Admin\Desktop\IFP - Mine\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Set the minimum confidence threshold for detecting objects
conf_threshold = 0.5

# Set the non-maximum suppression threshold for eliminating overlapping detections
nms_threshold = 0.4

# Open camera
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()

    # Create a blob from the input image
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), (0,0,0), True, crop=False)

    # Set the input for the neural network
    net.setInput(blob)

    # Get the output layer names
    output_layers = net.getUnconnectedOutLayersNames()

    # Run forward pass through the network
    outs = net.forward(output_layers)

    # Initialize lists for detected objects' class IDs, confidences, and bounding boxes
    class_ids = []
    confidences = []
    boxes = []

    # Loop over all detected objects
    for out in outs:
        for detection in out:
            # Get class ID and confidence
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak detections
            if confidence > conf_threshold:
                # Get the bounding box coordinates
                box = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (centerX, centerY, width, height) = box.astype("int")

                # Add the detected object's class ID, confidence, and bounding box to lists
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, int(width), int(height)])

    # Apply non-maximum suppression to eliminate overlapping detections
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # Draw the bounding boxes and labels for each detected object
    for i in indices:
        #i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
        color = (0,255,0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        voice = pyttsx3.init()
        voice.say(classes[class_ids[i]])
        voice.runAndWait()

        print(classes[class_ids[i]])
        
    # Display the resulting image
    cv2.imshow("object detection", frame)
    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
