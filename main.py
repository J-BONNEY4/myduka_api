from fastapi import FastAPI
from data_schemas import ProductRequest, ProductResponse
from models import Base, Product,User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


app = FastAPI()

engine=create_engine("sqlite:///./myduka_api.db",echo=True)

# creates tables
Base.metadata.create_all(engine)

session=Session(engine)

# def add_user():
#     user=User(
#         full_name="",
#         email="",
#         password="",
#         phone_number=""
#     )
#     session.add(user)
#     session.commit()

# Home Route 
@app.get("/")
def home():
    return {"Duka FastAPI Version": "1.0"}


@app.post("/products", response_model=ProductResponse)
def create_product(prod: ProductRequest):
    new_product = Product(
        user_id=prod.user_id,  # add user_id to ProductRequest
        product_name=prod.product_name,
        buying_price=prod.buying_price,
        selling_price=prod.selling_price,
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@app.get("/products", response_model=list[ProductResponse])
def get_products(user_id: int):
    query = select(Product).where(Product.user_id == user_id)
    return session.scalars(query).all()