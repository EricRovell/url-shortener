from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies.exceptions import raise_not_found
from ..database.db import get_db
from ..database.admin import get_admin_info
from ..database import crud

router = APIRouter(
	prefix="/admin",
	tags=["admin"],
)

@router.get(
	"/{secret_key}",
	name="administration_info",
	response_model=schemas.URLInfo
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
	"""
	Returns `URLInfo` of the shortened link by it's `secret_key`.
	"""
	if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
		return get_admin_info(db_url, request)
	else:
		raise_not_found(request)

@router.delete("/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
	"""
	Deletes a link by it's `secret_key`.
	"""
	if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key=secret_key):
		message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
		return { "detail": message }
	else:
		raise_not_found(request)
