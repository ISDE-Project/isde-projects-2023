from typing import List
from fastapi import Request


class TransformationForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.image_id: str
        self.color:float
        self.brightness:float 
        self.contrast:float 
        self.sharpness:float 

    async def load_data(self):
        form = await self.request.form()
        self.image_id = form.get("image_id")
        self.color = form.get('color')
        self.brightness = form.get('brightness')
        self.contrast = form.get('contrast')
        self.sharpness = form.get('sharpness')

    def is_valid(self):
            if not self.image_id or not isinstance(self.image_id, str):
                self.errors.append("A valid image id is required")
            self.cast_to_float()
            if self.errors:
                return False
            self.validate_float()
            if self.errors:
                return False
            return True


    def cast_to_float(self):
        try:
            self.color = float(self.color)
        except ValueError:
            self.errors.append("Datatype Error : color needs to be a float")
        try:
            self.brightness = float(self.brightness)
        except ValueError:
            self.errors.append("Datatype Error : brightness needs to be a float")
        try:
            self.contrast = float(self.contrast)
        except ValueError:
            self.errors.append("Datatype Error : contrast needs to be a float")
        try:
            self.sharpness = float(self.sharpness)
        except ValueError:
            self.errors.append("Datatype Error : sharpness needs to be a float")
    
    def validate_float(self):
        upper_bound=2.0
        lower_bound=0.0
        if  not(lower_bound <= self.color <= upper_bound) :
            self.errors.append(f"color only accepts floats between {lower_bound} and {upper_bound}")
        if  not(lower_bound <= self.brightness <= upper_bound) :
            self.errors.append(f"brightness only accepts floats between {lower_bound} and {upper_bound}")
        if  not(lower_bound <= self.contrast <= upper_bound) :
            self.errors.append(f"contrast only accepts floats between {lower_bound} and {upper_bound}")
        if  not(lower_bound <= self.sharpness <= upper_bound) :  
            self.errors.append(f"sharpness only accepts floats between {lower_bound} and {upper_bound}")  
    
    