
from datetime import datetime
from pydantic import BaseModel



class ProductRequest(BaseModel):
    user_id:int
    product_name: str
    buying_price: float
    selling_price: float

class ProductResponse(BaseModel):
    id: int
    user_id:int
    product_name: str
    buying_price: float
    selling_price: float
    created_at:datetime

class PurchaseRequest(BaseModel):
    product_id:int
    quantity:int
    paid_amount:float

class PurchaseResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    paid_amount:float
    created_at:datetime


class SaleRequest(BaseModel):
    user_id:int
    product_id:int
    quantity:int


class SaleResponse(BaseModel):
    id:int
    user_id:int
    product_id:int
    quantity:int
    created_at:datetime


class SaleDetailsRequest(BaseModel):
    product_id:int
    quantity:int

class SaleDetailsResponse(BaseModel):
    id:int
    sale_id:int
    product_id:int
    quantity:int
    unit_price:float#selling price  at the time of sale


class PaymentRequest(BaseModel):
    sale_id:int
    phone_number:str

class PaymentResponse(BaseModel):
    id:int
    sale_id:int
    amount:float
    trans_code:str | None
    mrid:str | None
    crid:str | None
    status:str
    phone_number:str
    created_at:datetime 
