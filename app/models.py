from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    branches = relationship("Branch", back_populates="bank")


class Branch(Base):
    __tablename__ = "branches"

    ifsc = Column(String, primary_key=True, index=True)
    branch = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    district = Column(String, nullable=True)
    state = Column(String, nullable=True)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False)

    bank = relationship("Bank", back_populates="branches")
