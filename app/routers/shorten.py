from fastapi import APIRouter, Depends, Request
from ..dependencies.exceptions import raise_bad_request
from .. import schemas
from ..database.db import get_db
from ..database.admin import get_admin_info
from ..database import crud
from sqlalchemy.orm import Session

from validators import url as validate_url

router = APIRouter(
	prefix="/shorten",
	tags=["url"],
)

@router.post("/", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, request: Request, db: Session = Depends(get_db)):
	"""
	Creates a short link for a given `target_url`.
	"""
	if not validate_url(url.target_url):
		raise_bad_request(message="Provided URL is not valid")

	db_url = crud.create_db_url(db=db, url=url)
	return get_admin_info(db_url, request)
