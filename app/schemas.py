from pydantic import BaseModel
from typing import Optional


class BankOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BranchOut(BaseModel):
    ifsc: str
    branch: str
    address: Optional[str]
    city: Optional[str]
    district: Optional[str]
    state: Optional[str]
    bank: BankOut

    class Config:
        orm_mode = True
