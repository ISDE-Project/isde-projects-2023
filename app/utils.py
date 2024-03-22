import os

from app.config import Configuration

conf = Configuration()


def list_images():
    """Returns the list of available images."""
    # img_names = filter(
    #     lambda x: x.endswith(".jpeg"), os.listdir(conf.image_folder_path)
    # )
    img_names = filter(
    lambda x: x.lower().endswith((".jpeg",".JPEG")), os.listdir(conf.image_folder_path)
)

    return list(img_names)
