from fastapi import FastAPI,HTTPException
from myjwt import create_access_token,verify_password,get_current_user
from data_schemas import ProductRequest, ProductResponse,PurchaseRequest,PurchaseResponse,SaleRequest,SaleResponse,SaleDetailsResponse,SaleDetailsRequest,PaymentResponse,PaymentRequest,PaymentUpdate
from models import Base, Product,Purchase,Sale,SaleDetail,Payment
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


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_single_product(product_id:int):
    query = select(Product).where(Product.id == product_id)
    products=session.scalars(query).first()

    if products is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return products

# path parameter(the one in curly braces) is useful when writing a query
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(prod : ProductRequest,product_id : int):
    query = select(Product).where(Product.id == product_id)
    products = session.scalars(query).first()
    if products is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    products.product_name=prod.product_name
    products.buying_price=prod.buying_price
    products.selling_price=prod.selling_price

    #session.add not needed since we aint adding a new product
    session.commit()

    return products
# end of products route.

# Purchases
@app.post("/purchases", response_model=PurchaseResponse)
def create_purchase(purch:PurchaseRequest):
    new_purchase=Purchase(
        product_id=purch.product_id,
        quantity=purch.quantity,
        paid_amount=purch.paid_amount

    )
    session.add(new_purchase)
    session.commit()
    return new_purchase

@app.get("/purchases", response_model=list[PurchaseResponse])
def get_purchases(product_id:int):
    query=select(Purchase).where(Purchase.product_id==product_id)
    return session.scalars(query).all()


@app.get("/purchase/{purchase_id}", response_model=PurchaseResponse)
def get_single_purchase(purchase_id : int):
    query = select(Purchase).where(Purchase.id == purchase_id)
    purchase=session.scalars(query).first()

    if purchase is None:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found"
        )
    return purchase

@app.put("/purchase/{purchase_id}",response_model=PurchaseResponse)
def update_purchase(purch : PurchaseRequest, purchase_id : int):
    query= select(Purchase).where(Purchase.id == purchase_id)
    purchase = session.scalars(query).first()
    if purchase is None:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found"
        )
    purchase.product_id=purch.product_id
    purchase.paid_amount=purch.paid_amount
    purchase.quantity=purch.quantity

    session.commit()

    return purchase
# End of purchase routes.

# sales routes
@app.post("/sales",response_model=SaleResponse)
def create_sale(sal:SaleRequest):
    new_sale=Sale(
        product_name =sal.product_name,
        amount=sal.amount
    )
    session.add(new_sale)
    session.commit()

    return new_sale

@app.get("/sales", response_model=list[SaleResponse])
def get_sales():
    query=select(Sale)
    sales=session.scalars(query).all()

    return sales

@app.get("/sales/{sales_id}", response_model=SaleResponse)
def get_single_sale(sales_id: int):
    query = select(Sale).where(Sale.id == sales_id)
    sales = session.scalars(query).first()

    if sales is None:
        raise HTTPException(
            status_code= 404,
            detail="Sale not found"
        )
    return sales

@app.put("/sales/{sales_id}", response_model=SaleResponse)
def update_sale(sal : SaleRequest, sales_id : int):
    query = select(Sale).where(Sale.id == sales_id)
    sales = session.scalars(query).first()

    if sales is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    sales.product_name = sal.product_name
    sales.amount = sal.amount

    session.commit()

    return sales
# End of sales routes


# sale_details routes
@app.post("/sales_details", response_model=SaleDetailsResponse, status_code=201)
def create_sale_detail(sale_details: SaleDetailsRequest):
    sale = session.get(Sale, sale_details.sale_id)
    if sale is None:
        raise HTTPException(
            status_code=404, 
            detail="Sale not found")

    product = session.get(Product, sale_details.product_id)
    if product is None:
        raise HTTPException(
            status_code=404, 
            detail="Product not found")

    db_sale_details = SaleDetail(
        product_id=sale_details.product_id,
        sale_id=sale_details.sale_id,
        quantity=sale_details.quantity,
        unit_price=product.selling_price,  # price at the time of sale
    )

    session.add(db_sale_details)
    session.commit()
    return db_sale_details


@app.get("/sales_details", response_model=list[SaleDetailsResponse])
def get_sales_details():
    query = select(SaleDetail)
    sales_details = session.scalars(query).all()

    return sales_details


@app.get("/sales_details/{sale_detail_id}", response_model=SaleDetailsResponse)
def get_single_sale_detail(sale_detail_id: int):
    query = select(SaleDetail).where(SaleDetail.id == sale_detail_id)
    sale_detail = session.scalars(query).first()

    if sale_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Sale detail not found"
        )

    return sale_detail


@app.put("/sales_details/{sale_detail_id}", response_model=SaleDetailsResponse)
def update_sale_detail(sale_details: SaleDetailsRequest, sale_detail_id: int):
    query = select(SaleDetail).where(SaleDetail.id == sale_detail_id)
    sale_detail = session.scalars(query).first()

    if sale_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Sale detail not found"
        )

    # only re-snapshot the price if the product changed
    if sale_detail.product_id != sale_details.product_id:
        product = session.get(Product, sale_details.product_id)
        if product is None:
            raise HTTPException(
                status_code=404, 
                detail="Product not found")
        sale_detail.unit_price = product.selling_price

    sale_detail.product_id = sale_details.product_id
    sale_detail.sale_id = sale_details.sale_id
    sale_detail.quantity = sale_details.quantity

    session.commit()
    session.refresh(sale_detail)
    return sale_detail
# End of sale_details routes

# payment route
@app.post("/payment", response_model=PaymentResponse)
def create_payment(pay: PaymentRequest):
    Tpay=Payment(
        sale_id=pay.sale_id,
        amount=pay.amount,
        trans_code=pay.trans_code,
        mrid=pay.mrid,
        crid=pay.crid,
        status=pay.status,
        phone_number=pay.phone_number
    )
    session.add(Tpay)
    session.commit()

    return Tpay

@app.get("/payment", response_model=list[PaymentResponse])
def get_payment():
    query=select(Payment)
    payments=session.scalars(query).all()
    return payments


@app.get("/payment/{payment_id}", response_model=PaymentResponse)
def get_single_payment(payment_id : int):
    query = select(Payment).where(Payment.id ==payment_id)
    payment = session.scalars(query).first()
    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )
    return payment

@app.put("/payment/{payment_id}", response_model=PaymentResponse)
def update_payment(pay:PaymentUpdate,payment_id:int):
    query=select(Payment).where(Payment.id == payment_id)
    payment = session.scalars(query).first()
    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="payment not found"
        )
    if pay.status not in ("pending","paid","failed"):
        raise HTTPException(
            status_code=404,
            detail="Status must be pending,paid or failed"
        )
    if pay.sale_id !=payment.sale_id and session.get(Sale,pay.sale_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )
    payment.sale_id=pay.sale_id
    payment.amount=pay.amount
    payment.trans_code=pay.trans_code
    payment.mrid=pay.mrid
    payment.crid = pay.crid
    payment.status = pay.status
    payment.phone_number = pay.phone_number

    session.commit()

    return payment

    

