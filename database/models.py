from sqlalchemy import ForeignKey, Column, Integer, String, Date, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base


class RentRequest(Base):
    __tablename__ = "rent_request"

    request_id = Column(Integer, primary_key=True, index=True, nullable=False)

    name = Column(String(50), nullable=False)
    phone_number = Column(String(12), nullable=False)
    wished_date_start = Column(Date, nullable=False)
    wished_date_end = Column(Date, nullable=False)
    wishings = Column(Text)

    contract = relationship("Contract", back_populates="rent_request")


class Contract(Base):
    __tablename__ = "contract"

    contract_id = Column(Integer, primary_key=True, index=True, nullable=False)

    datetime_start = Column(DateTime(timezone=True), nullable=False)
    datetime_end = Column(DateTime(timezone=True), nullable=False)
    is_paid = Column(Boolean, nullable=False)
    request_id = Column(Integer, ForeignKey('rent_request.request_id'), nullable=True)

    rent_request = relationship("RentRequest", back_populates="contract")
