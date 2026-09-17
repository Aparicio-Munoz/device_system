"""Modelos de base de datos.

Los imports de los modelos se mantienen aquí para que cualquier proceso que
necesite construir ``Base.metadata`` (por ejemplo, Alembic) registre todas las
tablas de la aplicación.
"""

from .device_model import Device
from .loan_model import Loan
from .user_model import User

__all__ = ["Device", "Loan", "User"]
