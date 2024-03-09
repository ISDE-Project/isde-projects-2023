from typing import List
from fastapi import Request

class HistogramForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.image_id: str
        self.histogram_type: str  # Add the histogram_type attribute

    async def load_data(self):
        form = await self.request.form()
        self.image_id = form.get("image_id")
        self.histogram_type = form.get("histogram_type")  # Load the histogram_type from the form

    def is_valid(self):
        if not self.image_id or not isinstance(self.image_id, str):
            self.errors.append("A valid image id is required")
        if not self.histogram_type or not isinstance(self.histogram_type, str):  # Validate histogram_type
            self.errors.append("A valid image type is required")
        if not self.errors:
            return True
        
        return False