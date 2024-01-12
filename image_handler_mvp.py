from PIL import Image

def cut_and_save_image(input_path, output_folder):
    # Open the image file
    image = Image.open(input_path)

    # Get the dimensions of the image
    width, height = image.size

    # Specify the size and shape of each piece
    pieces_info = [
        {"vertices": [(0, 0), (width // 3, 0), (width // 2, height), (0, height // 2)], "name": "piece_1"},
        {"vertices": [(width // 3, 0), (2 * width // 3, 0), (width // 2, height), (width // 3, height // 2)], "name": "piece_2"},
        {"vertices": [(2 * width // 3, 0), (width, 0), (width // 2, height), (2 * width // 3, height // 2)], "name": "piece_3"},
        {"vertices": [(0, height // 2), (width // 3, height // 2), (width // 2, height), (0, height)], "name": "piece_4"},
        {"vertices": [(width // 3, height // 2), (2 * width // 3, height // 2), (width // 2, height), (width // 3, height)], "name": "piece_5"},
        {"vertices": [(2 * width // 3, height // 2), (width, height // 2), (width // 2, height), (2 * width // 3, height)], "name": "piece_6"},
        {"vertices": [(0, height), (width // 3, height), (width // 2, height), (0, height // 2)], "name": "piece_7"}
    ]

    # Loop through the pieces info and cut the image
    for piece_info in pieces_info:
        # Get the vertices and name of the piece
        vertices = piece_info["vertices"]
        piece_name = piece_info["name"]

        # Print the coordinates of the vertices
        print(f"Vertices of {piece_name}: {vertices}")

        # Convert vertices to box coordinates
        left, upper, right, lower = min(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0]), \
                                   min(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1]), \
                                   max(vertices[0][0], vertices[1][0], vertices[2][0], vertices[3][0]), \
                                   max(vertices[0][1], vertices[1][1], vertices[2][1], vertices[3][1])

        # Crop the image to get a piece
        piece = image.crop((left, upper, right, lower))

        # Save the piece to the output folder
        piece.save(f"{output_folder}/{piece_name}.png")

if __name__ == "__main__":
    # Replace 'input_image.jpg' with the path to your input image file
    input_path = 'input_image.jpg'

    # Replace 'output_folder' with the desired output folder path
    output_folder = 'output'

    # Create the output folder if it doesn't exist
    import os
    os.makedirs(output_folder, exist_ok=True)

    # Call the function to cut and save the image
    cut_and_save_image(input_path, output_folder)
