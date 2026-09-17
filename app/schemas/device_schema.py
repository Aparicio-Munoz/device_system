from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _clean_text(value: str) -> str:
    return value.strip() if isinstance(value, str) else value


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    serial_number: str = Field(..., min_length=2, max_length=100)
    device_type: str = Field(..., min_length=2, max_length=50)
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool = True

    _clean_name = field_validator("name", mode="before")(_clean_text)
    _clean_serial = field_validator("serial_number", mode="before")(_clean_text)
    _clean_type = field_validator("device_type", mode="before")(_clean_text)
    _clean_brand = field_validator("brand", mode="before")(_clean_text)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2024-001",
                "device_type": "laptop",
                "brand": "Lenovo",
                "is_available": True,
            }
        }
    )


class DeviceUpdate(DeviceCreate):
    pass


class DevicePatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    serial_number: str | None = Field(default=None, min_length=2, max_length=100)
    device_type: str | None = Field(default=None, min_length=2, max_length=50)
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool | None = None

    _clean_name = field_validator("name", mode="before")(_clean_text)
    _clean_serial = field_validator("serial_number", mode="before")(_clean_text)
    _clean_type = field_validator("device_type", mode="before")(_clean_text)
    _clean_brand = field_validator("brand", mode="before")(_clean_text)


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: str | None
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceSummary(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)
