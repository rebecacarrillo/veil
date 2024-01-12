from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import base64
import io
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ImagePiece(db.Model):
    id = db.Column(db.String, primary_key=True)
    data = db.Column(db.LargeBinary)

def cut_and_save_image(encoded_image):
    # Decode the base64 encoded image
    decoded_image = base64.b64decode(encoded_image)

    # Open the image using PIL
    image = Image.open(io.BytesIO(decoded_image))

    # Get the dimensions of the image
    width, height = image.size

    # Specify the size and shape of each piece
    pieces_info = [
        # Define the vertices for each piece
        # Example: {"vertices": [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], "name": "piece_x"}
        # Adjust the vertices based on your requirement
    ]

    # Loop through the pieces info and cut the image
    for piece_info in pieces_info:
        vertices = piece_info["vertices"]

        # Convert vertices to box coordinates
        left, upper, right, lower = min(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0]), \
                                   min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1]), \
                                   max(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0]), \
                                   max(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1])

        # Crop the image to get a piece
        piece = image.crop((left, upper, right, lower))

        # Save the piece to the database
        image_id = str(uuid.uuid4())
        new_image_piece = ImagePiece(id=image_id, data=base64.b64encode(piece.tobytes()))
        db.session.add(new_image_piece)

    db.session.commit()

@app.route('/images', methods=['POST'])
def post_image():
    try:
        # Get the base64 encoded image from the request
        encoded_image = request.data.decode('utf-8')

        # Call the function to cut and save the image pieces
        cut_and_save_image(encoded_image)

        return jsonify({"message": "Success"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
