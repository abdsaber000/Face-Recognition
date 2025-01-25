import cv2
import matplotlib.pyplot as plt

img_path = "./images/test.jpg"

img = cv2.imread(img_path)

# convert image to grayscale to improve detection
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# haarcascade_frontalface_default.xml is a pre-trained model
# for detecting faces in images
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# perform face detection on gray scale image
face = face_classifier.detectMultiScale(
    gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)

# draw rectangle around detected face
for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

# convert image to RGB format
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

cv2.imwrite("./images/detected_face.jpg", img)