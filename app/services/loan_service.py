from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from ..models.device_model import Device
from ..models.loan_model import Loan
from ..models.user_model import User
from ..schemas.loan_schema import LoanCreate, LoanStatus
from .device_service import get_device
from .user_service import get_user


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_loan(db: Session, data: LoanCreate) -> Loan:
    user = get_user(db, data.user_id)
    device = get_device(db, data.device_id)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario está inactivo",
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo no está disponible",
        )

    loan = Loan(
        user_id=user.id,
        device_id=device.id,
        loan_date=data.loan_date or _now(),
        status="active",
    )
    device.is_available = False
    db.add(loan)

    try:
        db.commit()
        db.refresh(loan)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fue posible registrar el préstamo",
        ) from error

    return loan


def get_loan(db: Session, loan_id: int) -> Loan:
    statement = (
        select(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .where(Loan.id == loan_id)
    )
    loan = db.scalar(statement)

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado",
        )

    return loan


def list_loans(
    db: Session,
    loan_status: LoanStatus | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
    user_id: int | None = None,
    device_id: int | None = None,
    search: str | None = None,
) -> list[Loan]:
    statement = select(Loan).join(User, Loan.user_id == User.id).join(
        Device, Loan.device_id == Device.id
    )
    filters = []

    if loan_status is not None:
        filters.append(Loan.status == loan_status)
    if user_email is not None:
        filters.append(User.email.ilike(user_email))
    if device_type is not None:
        filters.append(Device.device_type.ilike(device_type))
    if user_id is not None:
        filters.append(Loan.user_id == user_id)
    if device_id is not None:
        filters.append(Loan.device_id == device_id)
    if search is not None:
        pattern = f"%{search}%"
        filters.append(
            or_(
                User.name.ilike(pattern),
                User.email.ilike(pattern),
                Device.name.ilike(pattern),
                Device.serial_number.ilike(pattern),
            )
        )

    if filters:
        statement = statement.where(and_(*filters))

    statement = statement.options(joinedload(Loan.user), joinedload(Loan.device))
    statement = statement.order_by(Loan.loan_date.desc(), Loan.id.desc())
    return list(db.scalars(statement).all())


def return_loan(db: Session, loan_id: int) -> Loan:
    loan = get_loan(db, loan_id)

    if loan.status == "returned" or loan.return_date is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo ya fue devuelto",
        )

    loan.status = "returned"
    loan.return_date = _now()
    loan.device.is_available = True

    try:
        db.commit()
        db.refresh(loan)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fue posible devolver el préstamo",
        ) from error

    return loan


def list_user_loans(db: Session, user_id: int) -> list[Loan]:
    get_user(db, user_id)
    return list_loans(db, user_id=user_id)


def list_device_loans(db: Session, device_id: int) -> list[Loan]:
    get_device(db, device_id)
    return list_loans(db, device_id=device_id)
