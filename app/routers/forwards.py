from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from ..dependencies.exceptions import raise_not_found
from ..database.db import get_db
from ..database import crud
from sqlalchemy.orm import Session

router = APIRouter(
	tags=["root"],
)

@router.get("/")
def read_root():
	return "Welcome to the URL shortener API"

@router.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
	"""
	Forwards to the link from given `url_key`, if present.
	"""
	if db_url:= crud.get_db_url_by_key(db=db, url_key=url_key):
		crud.update_db_clicks(db=db, db_url=db_url)
		return RedirectResponse(db_url.target_url)
	else:
		raise_not_found(request)
