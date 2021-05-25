import cv2
import numpy as np


# Load Yolo
net = cv2.dnn.readNet("yolov4-tiny-obj_6000.weights", "yolov4-tiny-obj.cfg")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# Classes
classes = ["drop", "left", "rotate", "right"]


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))




def detect_and_show(net):
    # Connecting cam and taking frames

    _, img = cap.read()

    img = cv2.resize(img, None, fx=0.8, fy=0.8)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 1.0 / 255, (352, 352), (0, 0, 0), True, crop=True)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    prediciton = ""

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                prediciton = classes[class_id]
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    return prediciton


cv2.destroyAllWindows()
