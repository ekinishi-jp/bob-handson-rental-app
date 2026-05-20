from pydantic import BaseModel, EmailStr, Field


class Property(BaseModel):
    id: int
    title: str
    building_name: str
    address: str
    station: str
    walk_minutes: int
    rent_yen: int
    management_fee_yen: int
    deposit_months: float
    key_money_months: float
    layout: str
    area_sqm: float
    built_year: int
    floor: str
    image_url: str
    amenities: list[str]
    availability: str
    description: str


class InquiryCreate(BaseModel):
    property_id: int
    name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(min_length=8)
    message: str = Field(min_length=1)


class Inquiry(BaseModel):
    id: int
    user_id: str
    property_id: int
    name: str
    email: EmailStr
    phone: str
    message: str
    created_at: str
