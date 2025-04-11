from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

class AssetSchema(BaseModel):
    id: Optional[int] = None
    asset_id: Optional[str] = None
    company: int
    location: int
    name: str
    category: str
    department: str
    assigned: str
    purchase_price: float
    purchase_date: date
    status: Optional[str] = None

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


class AssetTransferSchema(BaseModel):
    asset: int
    company: Optional[int] = None
    from_location: Optional[int] = None
    from_department: Optional[str] = None
    from_assigned: Optional[str] = None
    to_location: int
    to_department: str
    to_assigned: str
    transferred_by: str
    transfer_date: date
    status: str = "pending"
    note: Optional[str] = None

    class Config:
        from_attributes = True


class AssetDisposalSchema(BaseModel):
    asset: int
    company: Optional[int] = None
    method: str  # sale, scrap, donation
    disposal_date: date
    value_received: float
    note: Optional[str]
    approved_by: str

    class Config:
        from_attributes = True
