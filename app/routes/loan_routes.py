from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..dependencies.database_dependency import get_db
from ..schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanStatus
from ..services import loan_service


router = APIRouter(tags=["Loans"])


@router.post(
    "/loans",
    response_model=LoanDetailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar préstamo",
    response_description="Préstamo creado y dispositivo marcado como no disponible",
)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    created = loan_service.create_loan(db, loan)
    return loan_service.get_loan(db, created.id)


@router.get(
    "/loans/details",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos con usuario y dispositivo",
    response_description="Préstamos con información relacionada",
)
def list_loan_details(
    loan_status: LoanStatus | None = Query(default=None, alias="status"),
    user_email: str | None = Query(default=None),
    device_type: str | None = Query(default=None),
    user_id: int | None = Query(default=None, gt=0),
    device_id: int | None = Query(default=None, gt=0),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return loan_service.list_loans(
        db,
        loan_status,
        user_email,
        device_type,
        user_id,
        device_id,
        search,
    )


@router.get(
    "/loans",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos",
    response_description="Lista de préstamos filtrada",
)
def list_loans(
    loan_status: LoanStatus | None = Query(default=None, alias="status"),
    user_email: str | None = Query(default=None),
    device_type: str | None = Query(default=None),
    user_id: int | None = Query(default=None, gt=0),
    device_id: int | None = Query(default=None, gt=0),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return loan_service.list_loans(
        db,
        loan_status,
        user_email,
        device_type,
        user_id,
        device_id,
        search,
    )


@router.get(
    "/loans/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Consultar préstamo",
    response_description="Préstamo con usuario y dispositivo",
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loan(db, loan_id)


@router.patch(
    "/loans/{loan_id}/return",
    response_model=LoanDetailResponse,
    summary="Devolver dispositivo",
    response_description="Préstamo devuelto y dispositivo disponible",
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.return_loan(db, loan_id)


@router.get(
    "/users/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos de un usuario",
)
def list_user_loans(user_id: int, db: Session = Depends(get_db)):
    return loan_service.list_user_loans(db, user_id)


@router.get(
    "/devices/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar historial de un dispositivo",
)
def list_device_loans(device_id: int, db: Session = Depends(get_db)):
    return loan_service.list_device_loans(db, device_id)
