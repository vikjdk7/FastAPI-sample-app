from pydantic import BaseModel
from helper.tryenums import ModelName

class Items(BaseModel):
        id: str
        name: str
        category: str
        price: float
        quantity: int
        description: str
        inStock: bool
        model: ModelName
        tags: list
