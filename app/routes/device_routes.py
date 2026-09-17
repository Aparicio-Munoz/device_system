from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..dependencies.database_dependency import get_db
from ..schemas.device_schema import (
    DeviceCreate,
    DevicePatch,
    DeviceResponse,
    DeviceUpdate,
)
from ..services import device_service


router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    response_description="Dispositivo creado correctamente",
)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.create_device(db, device)


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    response_description="Lista de dispositivos filtrada",
)
def list_devices(
    device_type: str | None = Query(default=None),
    is_available: bool | None = Query(default=None),
    brand: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return device_service.list_devices(db, device_type, is_available, brand, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo",
    response_description="Dispositivo encontrado",
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    return device_service.get_device(db, device_id)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
)
def update_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
):
    return device_service.update_device(db, device_id, device)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar parcialmente un dispositivo",
)
def patch_device(
    device_id: int,
    device: DevicePatch,
    db: Session = Depends(get_db),
):
    return device_service.patch_device(db, device_id, device)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device_service.delete_device(db, device_id)
    return None
