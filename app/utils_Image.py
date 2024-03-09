from PIL import Image,ImageEnhance


def Transform_img(img_path,TransformationValues):
    img = Image.open(img_path)
    apply_brightness(img,10)
    apply_color(img,10)
    apply_contrast(img,10)
    apply_sharpness(img,10)
    return img

def apply_coloytttttttttttttttr(img, color):
    
    return img

def apply_brightness(img, brightness):
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness / 100.0)
    return img

def apply_contrast(img, contrast):
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast / 100.0)
    return img

def apply_sharpness(img, sharpness):
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness / 100.0)
    return img
