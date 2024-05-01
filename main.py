import json

from typing import Dict, List
from fastapi import FastAPI, Request , HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.forms.transformation_form import TransformationForm  
from app.forms.histogram_form import HistogramForm
from app.ml.classification_utils import classify_image , histogram_image
from app.utils import list_images
from app.utils_Image import Transform_img, encode_img_to_base64
from PIL import Image
import io


app = FastAPI()
config = Configuration()
imagenet_folder = "app/static/imagenet_subset"
json_file_path = "app/static/imagenet_subset/imagenet_labels.json"

    

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> Dict[str, List[str]]:
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The home page of the service."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classifications",)
def create_classify(request: Request):
    
    return templates.TemplateResponse(
        "classification_select.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )

# Issue No.3 download Results Button -------------------------------------------------------------------
@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    #The input parametre in the classify_image function is for making a difference between classifying local server images and user uploaded images
    classification_scores = classify_image(model_id=model_id, img_id=image_id,type='select')
    #Return the Classification Output Template which has client-side functionalities of downloading results -check "classification_output.html"
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )

# Issue No.2 Image Trasnformation -------------------------------------------------------------------
@app.get("/Transformations",)
def create_transform(request: Request):
    #The function simply returns the image transformation template 
    #The same template is used for displaying the form and also for displaying  transformation result
    #For the Get request the user expects only a form therefor a boolean variable ShowResult must be set to False
    return templates.TemplateResponse(
        "classification_Transform.html",
        {"request": request, "images": list_images(), "ShowResult":False},
    )

@app.post("/Transformations")
async def handle_transformations(request: Request):
    form = TransformationForm(request)
    await form.load_data()
    if not form.is_valid():
        return form.errors
    else:
        image_id = form.image_id
        #We pass the TransformationForm instance that contains all transformation settings received throught the request
        #Transform_img function returns the transform image in base64 format
        transformed_image_base64 = Transform_img(form)  
        
        #We return the image transformation Template
        #The same template is used for displaying the form and also for displaying  transformation result
        #The user expects the results therefor a boolean variable ShowResult must be set to True so that the transforlmation results part is rendered 
        #We pass the transformed image in its base64 format 
        return templates.TemplateResponse(
            "classification_Transform.html",
            {"request": request, "images": list_images(), 'imageId':image_id,'transformedImageBase64':transformed_image_base64, "ShowResult":True},
        )


# Issue No.1 Histogram -------------------------------------------------------------------
@app.get("/Histogram")
def create_histogram(request: Request):
    #Simply return the template containing the histogram form 
    return templates.TemplateResponse(
        "histogram.html",

        {"request": request, "images": list_images()},
    )


@app.post("/Histogram")
async def request_classification(request: Request):
    form = HistogramForm(request)
    await form.load_data()
    image_id = form.image_id 
    #Pass the id of the image we want to make a histogram for into the function : histogram_image
    #The function returns the HTML representation of the figure
    histograme_load = histogram_image(img_id=image_id)
    #Pass our parameters to the template and return it 
    return templates.TemplateResponse(
            "histogram_output.html",
            {
                "request": request,
                "image_id": image_id,
                "type": 'rgb',
                "histogram_plot": histograme_load,
            },
        )

# Issue No.4 Upload Image button -------------------------------------------------------------------
@app.get("/picture", response_class=HTMLResponse)
def picture(request: Request):
    
    return templates.TemplateResponse(
            "import_image.html",
            {"request": request, "models": Configuration.models},
        )
 
@app.post("/picture", response_class=HTMLResponse)
async def upload_and_classify(request: Request): 
    form=ClassificationForm(request)
    await form.load_data()
   
    try:
        # Open the image uploaded
        image = Image.open(io.BytesIO(form.uploaded_image))
        # Convert RGBA image to RGB if necessary
        if image.mode == 'RGBA':
            image = image.convert('RGB')
    except Exception as e:
          
        # If there's any other exception, raise an HTTPException with a generic error message
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

    image_base64 = encode_img_to_base64(image)
    model_id=form.model_id

    #Classify uploaded image using function classify_image
    #Set the input parameter type as 'upload' to indicate that the picture is user uploaded and not on the server
    #In this case the image ID input is set as the Image object we previously opened
    #By adding this type parametre to our classify image we can classify our uploaded images without adding any code 
    #We are simply reusing our classify_image function
    classification_scores = classify_image(model_id=model_id, img_id=image, type='upload')

    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": model_id,
            "image_base64": image_base64,  
            "type": 'upload',
            "classification_scores": json.dumps(classification_scores),
        },
    )
