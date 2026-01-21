from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.auth import get_current_user
from app.models import User, JobApplication
from app.schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

ALLOWED_STATUSES = {"applied", "interview", "offer", "rejected"}

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_value = payload.status.strip().lower()
    if status_value not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {sorted(ALLOWED_STATUSES)}",
        )

    app_row = JobApplication(
        user_id=current_user.id,
        company=payload.company.strip(),
        role_title=payload.role_title.strip(),
        status=status_value,
        location=(payload.location.strip() if payload.location else None),
        link=(payload.link.strip() if payload.link else None),
        notes=payload.notes,
    )
    db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return app_row


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    status: str | None = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(JobApplication).filter(JobApplication.user_id == current_user.id)

    if not include_inactive:
        q = q.filter(JobApplication.is_active == True)  # noqa: E712

    if status:
        status_value = status.strip().lower()
        if status_value not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status filter. Allowed: {sorted(ALLOWED_STATUSES)}",
            )
        q = q.filter(JobApplication.status == status_value)

    return q.order_by(JobApplication.applied_at.desc()).all()


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_row = (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id, JobApplication.user_id == current_user.id)
        .first()
    )
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_row


@router.patch("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_row = (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id, JobApplication.user_id == current_user.id)
        .first()
    )
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")

    data = payload.model_dump(exclude_unset=True)

    if "status" in data and data["status"] is not None:
        status_value = data["status"].strip().lower()
        if status_value not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Allowed: {sorted(ALLOWED_STATUSES)}",
            )
        data["status"] = status_value

    # Clean whitespace for some fields
    for field in ("company", "role_title", "location", "link"):
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip()

    for key, value in data.items():
        setattr(app_row, key, value)

    db.commit()
    db.refresh(app_row)
    return app_row


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app_row = (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id, JobApplication.user_id == current_user.id)
        .first()
    )
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")

    # Soft delete
    app_row.is_active = False
    db.commit()
    return None
