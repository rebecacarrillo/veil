from PIL import Image
from Fire import fire


def handle_image(path:str):
    """
    take in a supplied image path and do some cropping

    """

    img = Image.open(path)
    width, height = img.size

    sub_area = (0,0, width/2, height/2)
    cropped_img = img.crop(sub_area)

    cropped_img.save("cropped_picture.jpg")


if __name__ == "__main__":
    fire.handle_image()