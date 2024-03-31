import json
import os

import random
from typing import Dict, List
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import redis



from rq import Connection, Queue
from rq.job import Job

from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.forms.transformation_form import TransformationForm  
from app.forms.histogram_form import HistogramForm
from app.ml.classification_utils import classify_image , histogram_image
from app.utils import list_images
from app.utils_Image import Transform_img
import mpld3
from PIL import Image
import io
import base64

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



@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )


@app.get("/Transformations",)
def create_transform(request: Request):
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
        transformed_image_base64 = Transform_img(form)
        
        return templates.TemplateResponse(
            "classification_Transform.html",
            {"request": request, "images": list_images(), 'imageId':image_id,'transformedImageBase64':transformed_image_base64, "ShowResult":True},
        )



@app.get("/Histogram")
def create_histogram(request: Request):
    
    return templates.TemplateResponse(
        "histogram.html",

        {"request": request, "images": list_images()},
    )


@app.post("/Histogram")
async def request_classification(request: Request):
    form = HistogramForm(request)
    await form.load_data()
    image_id = form.image_id
    histogram_type = form.histogram_type  
    histograme_load = histogram_image(img_id=image_id)
    
    if histogram_type == 'rgb':
        types = 'rgb'
    else:
        types = 'gray'
        
    return templates.TemplateResponse(
            "histogram_output.html",
            {
                "request": request,
                "image_id": image_id,
                "type": types,
                "histogram_plot": histograme_load,
            },
        )

@app.get("/picture", response_class=HTMLResponse)
def picture(request: Request):
    
    return templates.TemplateResponse(
            "import_image.html",
            {"request": request, "models": Configuration.models},
        )
 
@app.post("/picture", response_class=HTMLResponse)
async def upload_and_classify(request: Request, model_id: str = Form(...), file: UploadFile = File(...)):
    
    image_contents = await file.read()
    image = Image.open(io.BytesIO(image_contents))
    image_base64 = base64.b64encode(image_contents).decode('utf-8')

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
