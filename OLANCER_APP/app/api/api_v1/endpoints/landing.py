from fastapi import APIRouter, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils import transpose
from .Repositories import repositories
from app.core import read_json

words = read_json.ReadJson()
templates = Jinja2Templates(directory="templates")

router = APIRouter()
rpos_context = repositories.Rpos()

@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def landing(request: Request):
    arr = []
    transpose(words.read_comment_home_cards(), arr)
    sample = rpos_context.get_context_home()
    sample.update({"comment_list": arr, "request": request})
    return templates.TemplateResponse(
        "home.html",
        context= sample
    )