import face_recognition

def load_and_encode_image(image_path):

    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) > 0:
        return face_encodings[0] 
    return None

def verify_user(encoding, registered_users):
    
    tolerance = 0.4
    for user_id, registered_encoding in registered_users.items():
        match = face_recognition.compare_faces(
            [registered_encoding],
            encoding,
            tolerance=tolerance
        )
        if match[0]:
            return user_id
    return None