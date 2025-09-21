from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import validators

from . import schemas, models

from .config import get_settings
from .database.db import engine, get_db
from .database import crud
from starlette.datastructures import URL
from .dependencies.exceptions import raise_bad_request, raise_not_found
from .routers import shorten, forwards, admin

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
	base_url = URL(get_settings().base_url)
	admin_endpoint = app.url_path_for(
		"administration_info", secret_key=db_url.secret_key
	)
	db_url.url = str(base_url.replace(path=db_url.key))
	db_url.admin_url = str(base_url.replace(path=admin_endpoint))
	return db_url

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(shorten.router)
app.include_router(forwards.router)
app.include_router(admin.router)
