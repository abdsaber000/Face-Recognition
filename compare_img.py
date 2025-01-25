import face_recognition

def load_and_encode_image(image_path):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if encoding:
        return encoding[0]
    else:
        return None
    
def save_user_image(image_name , user_id):
    with open("db.csv", "w") as db:
        db.write(f"{user_id},{image_name}\n")
        db.close()

def verify_user(image_encoding):
    with open("db.csv", "r") as db:
        for line in db:
            user_id, image_name = line.strip().split(",")
            encoding = load_and_encode_image(f"./images/{image_name}")
            results = face_recognition.compare_faces([encoding], image_encoding)
            if results[0]:
                return user_id
        return None

