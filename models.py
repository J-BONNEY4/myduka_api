from decimal import Decimal
from sqlalchemy import Integer, String, Float,DateTime,ForeignKey,Numeric
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship

class Base(DeclarativeBase):
      pass

class User(Base):
       __tablename__="users"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       full_name:Mapped[str]=mapped_column(String(100))
       email:Mapped[str]=mapped_column(String(100),unique=True)
       password:Mapped[str]=mapped_column(String(200))

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_name: Mapped[str] = mapped_column(String(100))
    buying_price: Mapped[float] = mapped_column(Float)
    selling_price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Purchase(Base):
       __tablename__="purchases"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("products.id"))
       # supplier_id:Mapped[int]=mapped_column(Integer)
       quantity:Mapped[int]=mapped_column(Integer)
       paid_amount:Mapped[float]=mapped_column(Float)
       created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
       

class Sale(Base):
       __tablename__="sales"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("products.id"))
       quantity:Mapped[int]=mapped_column(Integer,default=1)
       created_at:Mapped[DateTime]=mapped_column(DateTime,default=datetime.now)


class SaleDetail(Base):
       __tablename__="sale_details"
       id:Mapped[int]=mapped_column(Integer,primary_key=True)
       product_id:Mapped[int]=mapped_column(Integer,ForeignKey("products.id"))
       sale_id:Mapped[int]=mapped_column(Integer,ForeignKey("sales.id"))
       quantity:Mapped[int]=mapped_column(Integer)
       unit_price:Mapped[Decimal]=mapped_column(Numeric(10,2))


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id:Mapped[int]=mapped_column(ForeignKey("sales.id"))
    amount: Mapped[float] = mapped_column(Float)
#     method: Mapped[str] = mapped_column(String(70))
    trans_code:Mapped[str |None]=mapped_column(String(200),nullable=True)   #This tells SQLAlchemy that trans_code
#                                                                     can be None while the payment is pending.)
    status: Mapped[str] = mapped_column(String,default="pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    mrid:Mapped[str | None]=mapped_column(String(200))
    crid:Mapped[str | None]= mapped_column(String(200))
    phone_number:Mapped[str] =mapped_column(String(20))

