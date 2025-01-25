import face_recognition

def load_and_encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if encoding:
        return encoding[0]
    else:
        return None

# Load and encode the first image
img_path1 = "./images/test3.jpg"
encoding1 = load_and_encode_image(img_path1)

if encoding1 is None:
    print("couldn't find a face in image1")
    exit()

# Load and encode the second image
img_path2 = "./images/test4.jpg"
encoding2 = load_and_encode_image(img_path2)

if encoding2 is None:
    print("couldn't find a face in image2")
    exit()

print(encoding1 , '\n' , encoding2, '\n')

tolerance = 0.4
# Compare the faces
results = face_recognition.compare_faces([encoding1], encoding2 , tolerance=tolerance)
if results[0]:
    print("The images correspond to the same person.")
else:
    print("The images do not correspond to the same person.")