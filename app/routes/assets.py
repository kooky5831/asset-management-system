from fastapi import APIRouter, Depends, HTTPException
from app.models.assets import Asset, AssetTransfer, Maintenance, Vendor
from app.schemas.assets import AssetSchema, AssetTransferSchema, MaintenanceSchema, VendorSchema
from app.utils import success_response, error_response
from app.models.company import Company, Location
router = APIRouter()

# ✅ List & Create Assets
@router.get("/", response_model=list[AssetSchema])
async def list_assets():
    assets = await Asset.all()

    result = []
    for asset in assets:
        result.append({
            "id": asset.id,
            "asset_id": asset.asset_id,
            "company": asset.company_id, 
            "location": asset.location_id,  
            "name": asset.name,
            "category": asset.category,
            "department": asset.department,
            "assigned": asset.assigned,
            "purchase_price": asset.purchase_price,
            "purchase_date": asset.purchase_date,
            "status": asset.status
        })
    
    return result

@router.post("/", response_model=AssetSchema)
async def create_asset(asset_data: AssetSchema):
    # Get the related Company instance
    company = await Company.get(id=asset_data.company)
    location = await Location.get(id=asset_data.location)
    asset = await Asset.create(
        company=company,
        name=asset_data.name,
        location=location,
        category=asset_data.category,
        department = asset_data.department,
        assigned= asset_data.assigned,
        purchase_price=asset_data.purchase_price,
        purchase_date=asset_data.purchase_date,
    )
    
    return {
        "id": asset.id,
        "asset_id": asset.asset_id,
        "company": asset.company.id,
        "location": asset.location.id,
        "name": asset.name,
        "category": asset.category,
        "department": asset.department,
        "assigned": asset.assigned,
        "purchase_price": asset.purchase_price,
        "purchase_date": asset.purchase_date,
        "status": asset.status
    }

# ✅ Retrieve Asset by ID
@router.get("/{asset_id}", response_model=AssetSchema)
async def get_asset(asset_id: str):
    asset = await Asset.get_or_none(asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {
        "id": asset.id,
        "asset_id": asset.asset_id,
        "company": asset.company_id,
        "location": asset.location_id,
        "name": asset.name,
        "category": asset.category,
        "department": asset.department,
        "assigned": asset.assigned,
        "purchase_price": asset.purchase_price,
        "purchase_date": asset.purchase_date,
        "status": asset.status
    }

@router.post("/transfer", response_model=AssetTransferSchema)
async def transfer_asset(data: AssetTransferSchema):
    asset = await Asset.get(id=data.asset)
    
    from_location_id = asset.location_id
    from_department = asset.department
    from_assigned = asset.assigned
    company = await Company.get(id=data.company)
    from_location = None
    if from_location_id:
        from_location = await Location.get(id=from_location_id)
    
    to_location = await Location.get(id=data.to_location)

    asset.location = to_location
    asset.assigned = data.to_assigned
    asset.department = data.to_department
    
    await asset.save()
    
    transfer = await AssetTransfer.create(
        asset=asset,
        company=company,
        from_location=from_location,
        from_department=from_department,
        from_assigned=from_assigned,
        to_location=to_location,
        to_department=data.to_department,
        to_assigned=data.to_assigned,
        transferred_by=data.transferred_by,
        transfer_date=data.transfer_date,
        note=data.note or ""
    )
    
    return {
        "asset": asset.id,
        "company":company.id,
        "from_location": from_location_id,  
        "from_department": from_department,
        "from_assigned": from_assigned,
        "to_location": to_location.id,  
        "to_department": data.to_department,
        "to_assigned": data.to_assigned,
        "transferred_by": data.transferred_by,
        "transfer_date": data.transfer_date,
        "note": data.note or ""
    }

# ✅ List & Create Vendors
@router.get("/vendors", response_model=list[VendorSchema])
async def list_vendors():
    return await Vendor.all()

@router.post("/vendors", response_model=VendorSchema)
async def create_vendor(vendor_data: VendorSchema):
    vendor = await Vendor.create(**vendor_data.dict())
    return vendor

# ✅ List & Create Maintenance Records
@router.get("/maintenance", response_model=list[MaintenanceSchema])
async def list_maintenance():
    return await Maintenance.all()

@router.post("/maintenance", response_model=MaintenanceSchema)
async def create_maintenance(maintenance_data: MaintenanceSchema):
    maintenance = await Maintenance.create(**maintenance_data.dict())
    return maintenance
