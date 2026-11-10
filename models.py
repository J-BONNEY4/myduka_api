from sqlalchemy import Integer, String, Float,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from models import Base

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


    
