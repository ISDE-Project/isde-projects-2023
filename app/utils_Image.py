from PIL import Image,ImageEnhance
from app.forms.transformation_form import TransformationForm
from app.config import Configuration
import io
import base64
import os

conf = Configuration()

def Transform_img(form:TransformationForm) -> str:
    """
    Transforms the input image according to the specified parameters in the form.
    Args:
        form (TransformationForm): A form object containing transformation parameters.
    Returns:
        str: The transformed image encoded in base64 format.
    """
    image_path = os.path.join(conf.image_folder_path, form.image_id)
    # Decode and enhance the image
    
    img = Image.open(image_path)
    img = apply_color(img,form.color)
    img = apply_brightness(img,form.brightness)
    img = apply_contrast(img,form.contrast)
    img = apply_sharpness(img,form.sharpness)
    # Encode the enhanced image and return the result in base64 format 
    return encode_img_to_base64(img)


    


def apply_color(img, color_factor):
    #Takes and image and returns it with the applied color factor
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(color_factor)
    return img

def apply_brightness(img, brightness_factor):
    #Takes and image and returns it with the applied brightness factor
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(brightness_factor)
    return img

def apply_contrast(img, contrast_factor):
    #Takes and image and returns it with the applied contrast factor
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(contrast_factor)
    return img

def apply_sharpness(img, sharpness_factor):
    #Takes and image and returns it with the applied sharpeness factor
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(sharpness_factor)
    return img

def encode_img_to_base64(img):
    """
    Encodes the input image to base64 format.
    Args:
        img (PIL.Image): The input image.
    Returns:
        str: The base64 encoded string representing the image.
    """
    # Save the image to a BytesIO buffer
    output_buffer = io.BytesIO()
    img.save(output_buffer, format='jpeg')
     # Encode the image data as base64
    encoded_string = base64.b64encode(output_buffer.getvalue())
     # Decode the bytes to UTF-8 and return the result
    return encoded_string.decode('utf-8')