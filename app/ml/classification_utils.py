"""
This is a simple classification service. It accepts an url of an
image and returns the top-5 classification labels and scores.
"""
import importlib
import json
import logging
import os
import torch
import mpld3
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
from io import BytesIO


from app.config import Configuration


conf = Configuration()


def fetch_image(image_id):
    """Gets the image from the specified ID. It returns only images
    downloaded in the folder specified in the configuration object."""
    image_path = os.path.join(conf.image_folder_path, image_id)
    img = Image.open(image_path)
    return img


def get_labels():
    """Returns the labels of Imagenet dataset as a list, where
    the index of the list corresponds to the output class."""
    labels_path = os.path.join(conf.image_folder_path, "imagenet_labels.json")
    with open(labels_path) as f:
        labels = json.load(f)
    return labels


def get_model(model_id):
    """Imports a pretrained model from the ones that are specified in
    the configuration file. This is needed as we want to pre-download the
    specified model in order to avoid unnecessary waits for the user."""
    if model_id in conf.models:
        try:
            module = importlib.import_module("torchvision.models")
            return module.__getattribute__(model_id)(weights="DEFAULT")
        except ImportError:
            logging.error("Model {} not found".format(model_id))
    else:
        raise ImportError




def classify_image(model_id, img_id):
    """Returns the top-5 classification score output from the
    model specified in model_id when it is fed with the
    image corresponding to img_id."""
    img = fetch_image(img_id)
    model = get_model(model_id)
    
    model.eval()
    transform = transforms.Compose(
        (
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        )
    )

    # apply transform from torchvision
    img = img.convert("RGB")
    preprocessed = transform(img).unsqueeze(0)

    # gets the output from the model
    out = model(preprocessed)
    _, indices = torch.sort(out, descending=True)

    # transforms scores as percentages
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100

    # gets the labels
    labels = get_labels()

    # takes the top-5 classification output and returns it
    # as a list of tuples (label_name, score)
    output = [[labels[idx], percentage[idx].item()] for idx in indices[0][:5]]

    img.close()
    return output



def histogram_image(img_id):    
    img1 = fetch_image(img_id)
    
    # Convert Pillow JpegImageFile to NumPy array
    img_array = np.array(img1)

    r = img_array[:, :, 0]
    g = img_array[:, :, 1]
    b = img_array[:, :, 2]

    plt.subplots_adjust(hspace=0.5, wspace=0.2)

    # plt.subplot(2, 2, 1)
    # plt.title('Original Image')
    # plt.imshow(img_array)

    plt.subplot(2, 2, 1)
    plt.title('Red Histogram')
    hist, bins = np.histogram(r.ravel(), bins=256, range=(0, 255))
    plt.bar(bins[:-1], hist)

    plt.subplot(2, 2, 2)
    plt.title('Green Histogram')
    hist, bins = np.histogram(g.ravel(), bins=256, range=(0, 255))
    plt.bar(bins[:-1], hist)

    plt.subplot(2, 2, 3)
    plt.title('Blue Histogram')
    hist, bins = np.histogram(b.ravel(), bins=256, range=(0, 255))
    plt.bar(bins[:-1], hist)

    # Convert the matplotlib figure to HTML using mpld3
    fig_html = mpld3.fig_to_html(plt.gcf())

    return fig_html
