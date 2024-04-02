from PIL import Image,ImageEnhance
from app.forms.transformation_form import TransformationForm
from app.config import Configuration
import io
import base64
import os

conf = Configuration()

def Transform_img(form:TransformationForm) -> str:
    image_path = os.path.join(conf.image_folder_path, form.image_id)
    with open(image_path, "rb") as image_file:
         image_data = image_file.read()
    # Decode and enhance the image
    img = Image.open(io.BytesIO(image_data))
    img = Image.open(image_path)
    img = apply_color(img,form.color)
    img = apply_brightness(img,form.brightness)
    img = apply_contrast(img,form.contrast)
    img = apply_sharpness(img,form.sharpness)
    # Encode the enhanced image
    return encode_img_utf8(img)


    


def apply_color(img, color_factor):
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(color_factor)
    return img

def apply_brightness(img, brightness_factor):
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(brightness_factor)
    return img

def apply_contrast(img, contrast_factor):
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(contrast_factor)
    return img

def apply_sharpness(img, sharpness_factor):
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(sharpness_factor)
    return img

def encode_img_utf8(img):
    output_buffer = io.BytesIO()
    img.save(output_buffer, format='jpeg')
    encoded_string = base64.b64encode(output_buffer.getvalue())
    return encoded_string.decode('utf-8')
