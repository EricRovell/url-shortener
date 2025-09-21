from .. import schemas, models

from ..config import get_settings
from fastapi import Request

from starlette.datastructures import URL

def get_admin_info(db_url: models.URL, request: Request) -> schemas.URLInfo:
	base_url = URL(get_settings().base_url)
	print(db_url.secret_key)
	admin_endpoint = request.url_for(
		"administration_info", secret_key=db_url.secret_key
	)
	db_url.url = str(base_url.replace(path=db_url.key))
	db_url.admin_url = str(admin_endpoint)
	return db_url
