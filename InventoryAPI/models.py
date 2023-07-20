from pydantic import BaseModel, validator

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    @validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        return value

    @validator('quantity')
    def validate_quantity(cls, value):
        if value < 0:
            raise ValueError("Quantity must be greater than zero")
        return value
