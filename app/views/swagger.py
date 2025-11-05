from fastapi import APIRouter, Request, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

router = APIRouter()

open_api_url = "/openapi.json"

@router.get("/docs", include_in_schema=False)
async def custom_docs_html():
    """여기에 html 문서자체를 커스텀 마이징하는 로직을 추가하면 된다.
    CSRF_TOKEN을 주입하는 경우 등..."""
    return get_swagger_ui_html(
        openapi_url=open_api_url,  # openapi 스펙 파일 URL
        title="Custom API Docs",
    )


@router.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    """여기에 html 문서자체를 커스텀 마이징하는 로직을 추가하면 된다."""
    return get_redoc_html(
        openapi_url=open_api_url,   # 스펙 파일 경로
        title="Custom ReDoc",          # 페이지 제목
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )