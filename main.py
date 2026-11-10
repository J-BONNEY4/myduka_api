from fastapi import FastAPI
from data_schemas import ProductRequest, ProductResponse
from models import Base,Product,User
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker,declarative_base


app = FastAPI()


# Database URL
DATABASE_URL = "sqlite:///./myduka_api.db"

# Connect sql to the engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread" :False}
)
# Create Base
Base = declarative_base()

# scoped_session gives each request its own session
SessionLocal = sessionmaker(
     autocommit=False,
     autoflush=False,
     bind=engine
)

# creates tables.
Base.metadata.create_all(engine)
@app.get("/")
def home():
    return {"Duka FastAPI Version": "1.0"}

# user.
# @app.post("/users", response_model=UserResponse)
# def create_user(user: UserRequest):

#     db = SessionLocal()
#     new_user = User(
#         full_name=user.full_name,
#         email=user.email,
#         password=user.password
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     db.close()

#     return new_user


@app.post("/products", response_model=ProductResponse)
def create_product(prod: ProductRequest):
    new_product = Product(
        product_name=prod.product_name,
        buying_price=prod.buying_price,
        selling_price=prod.selling_price
    )
    SessionLocal.add(new_product)
    SessionLocal.commit()
    SessionLocal.refresh(new_product)

    return new_product

@app.get("/products", response_model=list[ProductResponse])
def get_products(user_id:int):
        db=SessionLocal()
        query = select(Product).where(Product.user_id == user_id)
        products = db.scalars(query)
        return products
