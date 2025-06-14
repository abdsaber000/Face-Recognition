from flask import request, jsonify, Flask
from services import load_and_encode_image, verify_user
from models import User, db
import json
import os
import uuid
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///face_recognition.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/register', methods=['POST'])
def register():
    
    if 'user_id' not in request.form:
        return jsonify({'message': 'user_id is required'}), 400

    if 'image' not in request.files:
        return jsonify({'message': 'image is required'}), 400

    user_id = request.form['user_id']
    image = request.files['image']

    if image.filename == '':
        return jsonify({'message': 'No selected image file'}), 400

    ext = os.path.splitext(image.filename)[1]
    hashed_name = hashlib.sha256((image.filename + str(uuid.uuid4())).encode()).hexdigest()
    filename = f"{hashed_name}{ext}"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    encoding = load_and_encode_image(image_path)
    if encoding is None:
        return jsonify({'message': 'No face detected in the image'}), 400

    registered_users = {user.user_id: json.loads(user.encoding) for user in User.query.all()}

    current_id = verify_user(encoding, registered_users)

    if current_id:
        if current_id != user_id:
            return jsonify({'message': 'Face already registered with a different user ID.'}), 400
        else:
            return jsonify({'message': 'User is already registered.'}), 200

    new_user = User(user_id=user_id, encoding=json.dumps(encoding.tolist()))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/verify', methods=['POST'])
def verfiy():
    if 'image' not in request.files:
        return jsonify({'message': 'image is required'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'message': 'No selected image file'}), 400

    ext = os.path.splitext(image.filename)[1]
    hashed_name = hashlib.sha256((image.filename + str(uuid.uuid4())).encode()).hexdigest()
    filename = f"{hashed_name}{ext}"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    encoding = load_and_encode_image(image_path)
    if encoding is None:
        return jsonify({'message': 'No face detected in the image'}), 400

    registered_users = {user.user_id: json.loads(user.encoding) for user in User.query.all()}

    user_id = verify_user(encoding, registered_users)
    if user_id:
        return jsonify({
            'data': {'user_id': user_id}
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User has been deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)