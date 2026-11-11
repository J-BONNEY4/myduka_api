
from datetime import datetime
from pydantic import BaseModel,Field



class ProductRequest(BaseModel):
    user_id:int
    product_name: str
    buying_price: float
    selling_price: float
    created_at:datetime = Field(default_factory=datetime.now)

class ProductResponse(BaseModel):
    id: int
    product_name: str
    buying_price: float
    selling_price: float
    # stock_quantity: int
    created_at:datetime = Field(default_factory=datetime.now)

