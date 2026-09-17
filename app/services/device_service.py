from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.device_model import Device
from ..schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def _values(data: DeviceCreate | DeviceUpdate | DevicePatch) -> dict[str, Any]:
    return data.model_dump(exclude_unset=True)


def _find_by_serial(
    db: Session,
    serial_number: str,
    device_id: int | None = None,
) -> Device | None:
    statement = select(Device).where(Device.serial_number == serial_number)

    if device_id is not None:
        statement = statement.where(Device.id != device_id)

    return db.scalar(statement)


def _commit(db: Session, device: Device) -> Device:
    try:
        db.commit()
        db.refresh(device)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado",
        ) from error

    return device


def create_device(db: Session, data: DeviceCreate) -> Device:
    values = _values(data)

    if _find_by_serial(db, values["serial_number"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado",
        )

    device = Device(**values)
    db.add(device)
    return _commit(db, device)


def list_devices(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
) -> list[Device]:
    statement = select(Device)

    if device_type is not None:
        statement = statement.where(Device.device_type.ilike(device_type))

    if is_available is not None:
        statement = statement.where(Device.is_available == is_available)

    if brand is not None:
        statement = statement.where(Device.brand.ilike(brand))

    if search is not None:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(
                Device.name.ilike(pattern),
                Device.serial_number.ilike(pattern),
                Device.device_type.ilike(pattern),
                Device.brand.ilike(pattern),
            )
        )

    statement = statement.order_by(Device.created_at, Device.id)
    return list(db.scalars(statement).all())


def get_device(db: Session, device_id: int) -> Device:
    device = db.get(Device, device_id)

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado",
        )

    return device


def update_device(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    device = get_device(db, device_id)
    values = _values(data)

    if _find_by_serial(db, values["serial_number"], device_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado",
        )

    for field, value in values.items():
        setattr(device, field, value)

    return _commit(db, device)


def patch_device(db: Session, device_id: int, data: DevicePatch) -> Device:
    device = get_device(db, device_id)
    values = _values(data)

    if not values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )

    if "serial_number" in values and _find_by_serial(
        db, values["serial_number"], device_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado",
        )

    for field, value in values.items():
        setattr(device, field, value)

    return _commit(db, device)


def delete_device(db: Session, device_id: int) -> None:
    device = get_device(db, device_id)

    if device.loans:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un dispositivo con historial de préstamos",
        )

    db.delete(device)

    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el dispositivo porque tiene préstamos",
        ) from error
