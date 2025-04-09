from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class AssetSchema(BaseModel):
    company: int
    name: str
    asset_id: Optional[str] = None
    category: str
    location: Optional[int]
    purchase_price: float
    purchase_date: date

    class Config:
        from_attributes = True

class VendorSchema(BaseModel):
    company: int
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]
    service_categories: str
    status: str

    class Config:
        from_attributes = True

class MaintenanceSchema(BaseModel):
    asset: int
    company: int
    maintenance_type: str
    description: str
    scheduled_date: date
    cost: float
    vendor: Optional[int]
    status: str

    class Config:
        from_attributes = True
