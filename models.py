from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # добавляем корень проекта
from database.db import Base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db import get_session

class ProductStatus(str, enum.Enum):
    processing = "В обработке"
    pending = "Ожидает выкладки"
    posted = "Выложен"
    canceled = "Отменен"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True)
    name = Column(String)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    products = relationship("Product", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.tg_id"))
    url = Column(String)
    name = Column(String)
    description = Column(Text)  # можно хранить длинный текст
    image_url = Column(String)

    # Новые поля
    wb_id = Column(Integer, nullable=True)            # артикула/ID WB
    brand = Column(String, nullable=True)
    seller = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    feedbacks = Column(Integer, nullable=True)
    basic_price = Column(Float, nullable=True)
    discount = Column(Integer, nullable=True)
    stocks = Column(Integer, nullable=True)
    stocks_by_size = Column(JSON, nullable=True)      # json array
    images = Column(JSON, nullable=True)              # json array (список url)

    info = Column(JSON, nullable=True)                # доп. JSON
    status = Column(Enum(ProductStatus), default=ProductStatus.processing)
    scheduled_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    price = Column(Float)

    user = relationship("User", back_populates="products")