"""
GET   /admin/users
GET   /admin/users/{user_id}
GET   /admin/roles
PATCH /admin/users/{user_id}/role

Every route here requires get_current_admin -- authenticated AND the
token's role claim is ADMIN. A student or teacher token gets 403, even if
that same person was promoted to admin a moment ago and even if their DB
row's live role has since changed -- see api/deps.py for why that's
deliberate (same reasoning as every other role check in this project).

There is no POST /admin/users/{id}/promote or /demote here on purpose --
the issue is explicit that this should be ONE generic role-change
operation, not a separate endpoint per transition.
"""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.models.role import UserRole
from app.models.user import User
from app.schemas.admin import RoleAssignment, RolePublic, UserAdminView
from app.services import admin_service, role_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserAdminView])
def list_users(
    role: UserRole | None = Query(default=None, description="Filter by role"),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return admin_service.list_users(db, role=role)


@router.get("/users/{user_id}", response_model=UserAdminView)
def get_user(
    user_id: uuid.UUID,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return admin_service.get_user(db, user_id)


@router.get("/roles", response_model=list[RolePublic])
def list_roles(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return role_service.list_roles(db)


@router.patch("/users/{user_id}/role", response_model=UserAdminView)
def change_user_role(
    user_id: uuid.UUID,
    payload: RoleAssignment,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return admin_service.set_user_role(db, target_user_id=user_id, new_role=payload.role)
