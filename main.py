from fastapi import FastAPI
from data_schemas import ProductRequest, ProductResponse
from models import Product
from database import session, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"Duka FastAPI Version": "1.0"}


@app.post("/products", response_model=ProductResponse)
def create_product(prod: ProductRequest):

    new_product = Product(
        product_name=prod.product_name,
        buying_price=prod.buying_price,
        selling_price=prod.selling_price
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product
