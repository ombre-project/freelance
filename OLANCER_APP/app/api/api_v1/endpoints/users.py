import datetime
import uuid
from typing import Any, List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email, WalletOlancer
from fastapi.templating import Jinja2Templates
from app.core import read_json
from .Repositories import repositories
from app.schemas.user import UserProf
from app.schemas.project import ProjectProf, ProjectTaken, ProjectFinal
import os
from app.utils import handle_uploaded_file, handle_uploaded_file_project, row2dict
from fastapi_pagination import paginate, pagination_params, Params


router = APIRouter()
templates = Jinja2Templates(directory="templates")
words = read_json.ReadJson()
rpos_context = repositories.Rpos()
ombre = WalletOlancer(ip=words.read_ombre_ip(), port=str(words.read_ombre_port()))


@router.get("/signup", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def signup_user(request: Request):
    sample = rpos_context.get_context_signup()
    sample.update({"request": request})
    return templates.TemplateResponse(
        "signup.html", context=sample
    )

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user


@router.post("/open", response_class=RedirectResponse)
async def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    re_password: str = Form(...),
) -> Any:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    if password != re_password:
        raise HTTPException(
            status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            detail="passwords you entered are not same !"
        )
    try:
        password_omb = str(uuid.uuid4())
        username_omb = str(uuid.uuid4())
        res = ombre.create_wallet(username=username_omb, password=password_omb)
        res = ombre.check_wallet(username=username_omb, password=password_omb)
        print(res)
        wallet_address = res["address"]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this user exist in ombre node!"
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=username, wallet_address=wallet_address, password_omb=password_omb, username_omb=username_omb)
    user = crud.user.create(db, obj_in=user_in)
    res = RedirectResponse(url="/api/v1/login", status_code=status.HTTP_302_FOUND)
    return res


@router.get("/{user_id}/wallet", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def wallet(
    req: Request,
    user_id: int,
    db: Session = Depends(deps.get_db)
):
    sample_user = crud.user.get(db=db, id=user_id)
    res = ombre.check_wallet(username=sample_user.username_omb, password=sample_user.password_omb)
    sample = rpos_context.get_context_wallet(words.read_api_prev_url(), user_id)
    print(res["balance"])
    sample.update({"request": req, "wallet_address": words.read_ombre_wallet_address()+str(sample_user.wallet_address), "wallet_balance": words.read_ombre_balance()+str(float(res["balance"])/(10**9)), "USER_ID": str(user_id)})
    return templates.TemplateResponse(
        "wallet.html", context=sample
    )


@router.post("/{user_id}/wallet", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def wallet(
    req: Request,
    user_id: int,
    db: Session = Depends(deps.get_db),
    credit: int = Form(...),
    wallet_address: str = Form(...)
):
    sample_user = crud.user.get(db=db, id=user_id)
    res = ombre.check_wallet(username=sample_user.username_omb, password=sample_user.password_omb)
    sample = rpos_context.get_context_wallet(words.read_api_prev_url(), user_id)
    print(res["balance"])
    if int(res["balance"]) > credit:
        ombre.transfer_to_address(username=sample_user.username_omb, password=sample_user.password_omb, address=wallet_address, amount=credit)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="your balance is less than your request !!!"
        )
    sample.update({"request": req, "wallet_address": words.read_ombre_wallet_address()+str(sample_user.wallet_address), "wallet_balance": words.read_ombre_balance()+str(float(res["balance"])/(10**9)), "USER_ID": str(user_id)})
    return templates.TemplateResponse(
        "wallet.html", context=sample
    )

@router.get("/{user_id}/profile", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def read_user_by_id(
    req: Request,
    user_id: int,
    db: Session = Depends(deps.get_db),
):
    user = crud.user.get_complete_user(db, id=user_id)
    if user.img_address is not None:
        src_img = user.img_address
    else:
        src_img = words.read_profile_img_prof()
    fname = user.full_name
    rl = user.resume_address
    burn = user.born
    wa = user.wallet_address
    ib = user.bio
    ia = user.address
    ic = user.city
    icountry = user.country
    sample = rpos_context.get_context_profile(words.read_api_prev_url(), user_id)
    list_projects_dev_final = crud.project.get_projects_dev_finish(db=db, id=user_id)
    list_projects_dev = crud.project.get_projects_not_dev_finish(db=db, id=user_id)
    list_projects_def_final = crud.project.get_projects_def_finish(db=db, id=user_id)
    list_projects_def = crud.project.get_projects_def_not_finish(db=db, id=user_id)
    sample.update({"prof_img": src_img,
                   "input_fname": fname,
                   "input_burn": burn,
                   "resume_link": rl,
                   "input_owa": wa,
                   "ID_USER": user_id,
                   "input_bio": ib,
                   "input_address": ia,
                   "input_city": ic,
                   "input_country": icountry,
                   "list_projects_dev_final": list_projects_dev_final,
                   "list_projects_dev": list_projects_dev,
                   "list_projects_def_final": list_projects_def_final,
                   "list_projects_def": list_projects_def,
                   "request": req})

    return templates.TemplateResponse(
        "profile.html", context=sample
    )

@router.post("/{user_id}/profile", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def read_user_by_id(
    req: Request,
    user_id: int,
    db: Session = Depends(deps.get_db),
    image: UploadFile = File(...),
    resume: UploadFile = File(...),
    res: UserProf = Depends(UserProf.as_form)
    ):
    user_smp = crud.user.get(db=db, id=user_id)
    try:
        if resume.content_type.split('/')[1] != "octet-stream":
            os.remove(os.getcwd() + "/statics/file/" + str(user_smp.resume_address).split("/")[4])
        if image.content_type.split('/')[1] != "octet-stream":
            os.remove(os.getcwd() + "/statics/images/" + str(user_smp.img_address).split("/")[4])
    except Exception as e:
        print(e)

    if resume.content_type.split('/')[1] != "octet-stream":
        res.resume_address = handle_uploaded_file(resume.file, str(datetime.datetime.today()), 'file', resume.content_type.split('/')[1])
    else:
        res.resume_address = user_smp.resume_address
    if image.content_type.split('/')[1] != "octet-stream":
        res.img_address = handle_uploaded_file(image.file, str(datetime.datetime.today()), 'images', image.content_type.split('/')[1])
    else:
        res.img_address = user_smp.img_address
    crud.user.update_complete_user(db=db, id=user_id, obj_in=res, db_obj=user_smp)
    user = crud.user.get_complete_user(db, id=user_id)
    if user.img_address is not None:
        src_img = user.img_address
    else:
        src_img = words.read_profile_img_prof()

    fname = user.full_name
    rl = user.resume_address
    burn = user.born
    wa = user.wallet_address
    ib = user.bio
    ia = user.address
    ic = user.city
    icountry = user.country
    sample = rpos_context.get_context_profile(words.read_api_prev_url(), user_id)
    sample.update({"prof_img": src_img,
                   "input_fname": fname,
                   "input_burn": burn,
                   "resume_link": rl,
                   "input_owa": wa,
                   "ID_USER": user_id,
                   "input_bio": ib,
                   "input_address": ia,
                   "input_city": ic,
                   "input_country": icountry,
                   "request": req})
    return templates.TemplateResponse(
        "profile.html", context=sample
    )

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

# ,Depends(deps.get_current_active_user)
@router.get("/{user_id}/project", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(pagination_params)])
def project(request: Request,
            user_id: int,
            db: Session = Depends(deps.get_db),
            params: Params = Depends()
):
    params.size = 4
    list_of_projects = paginate(sequence=crud.project.get_all_projects_not_finish(db=db, user_id=user_id), params=params).dict()
    sample = rpos_context.get_context_project(words.read_api_prev_url(), user_id)
    if list_of_projects['page'] >= list_of_projects['total']//params.size:
        list_of_projects['page'] = list_of_projects['total']//params.size
    sample.update({"ID_USER": user_id,
                   "list_p": list_of_projects['items'],
                   "request": request,
                   "total": list_of_projects['total'],
                   "page": list_of_projects['page']})
    return templates.TemplateResponse(
        "projects.html",
        context=sample
    )


@router.post("/{user_id}/project-lancer", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project(request: Request,
            user_id: int,
            res: ProjectProf = Depends(ProjectProf.as_form),
            db: Session = Depends(deps.get_db),
            file: UploadFile = File(...),
            img: UploadFile = File(...),
            params: Params = Depends()
):
    res.file_addr = handle_uploaded_file(file.file, str(datetime.datetime.today()), 'projects/file',
                                                  file.content_type.split('/')[1])
    res.img_addr = handle_uploaded_file(img.file, str(datetime.datetime.today()), 'projects/images',
                                               img.content_type.split('/')[1])
    res.project_offer_id = user_id
    res.start_date = datetime.datetime.today().strftime('%Y-%m-%d')
    crud.project.create(db=db, obj_in=res)
    params.size = 4
    list_of_projects = paginate(sequence=crud.project.get_all_projects_not_finish(db=db, user_id=user_id), params=params).dict()
    sample = rpos_context.get_context_project(words.read_api_prev_url(), user_id)
    if list_of_projects['page'] >= list_of_projects['total'] // params.size:
        list_of_projects['page'] = list_of_projects['total'] // params.size
    sample.update({"ID_USER": user_id,
                   "list_p": list_of_projects['items'],
                   "request": request,
                   "total": list_of_projects['total'],
                   "page": list_of_projects['page']})
    return templates.TemplateResponse(
        "projects.html",
        context=sample
    )

# , dependencies=[Depends(deps.get_current_active_user)]
@router.post("/{user_id}/project-search", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def project_search(request: Request,
            user_id: int,
            query: Optional[str] = Form(...),
            db: Session = Depends(deps.get_db),
            params: Params = Depends()
):
    params.size = 4
    list_of_projects = paginate(sequence=crud.project.search_project(db=db, query=query, user_id=user_id), params=params).dict()
    sample = rpos_context.get_context_project(words.read_api_prev_url(), user_id)
    if list_of_projects['page'] >= list_of_projects['total'] // params.size:
        list_of_projects['page'] = list_of_projects['total'] // params.size
    sample.update({"ID_USER": user_id,
                   "list_p": list_of_projects['items'],
                   "request": request,
                   "total": list_of_projects['total'],
                   "page": list_of_projects['page']})
    return templates.TemplateResponse(
        "projects.html",
        context=sample
    )




@router.post("/{user_id}/project-accepted/{project_id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project(request: Request,
            user_id: int,
            project_id: int,
            db: Session = Depends(deps.get_db),
            params: Params = Depends(),
            p: ProjectTaken = Depends()
):
    params.size = 4
    proj_sample = crud.project.get(db=db, id=project_id)
    p = row2dict(row=proj_sample, p=p)
    directory = os.getcwd()+f"/statics/projects/users_projects/{proj_sample.project_offer_id}"
    if not proj_sample.is_taken:
        p.project_owner_id = user_id
        p.is_taken = True
        if not os.path.exists(directory):
            os.mkdir(directory)
        p.address_of_project_uploaded = f"/../statics/projects/users_projects/{proj_sample.project_offer_id}"
        crud.project.take_project(db=db, id=project_id, db_obj=proj_sample, obj_in=p)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project already taken !"
        )
    list_of_projects = paginate(sequence=crud.project.get_all_projects_not_finish(db=db,user_id=user_id), params=params).dict()
    sample = rpos_context.get_context_project(words.read_api_prev_url(), user_id)
    if list_of_projects['page'] >= list_of_projects['total'] // params.size:
        list_of_projects['page'] = list_of_projects['total'] // params.size
    sample.update({"ID_USER": user_id,
                   "list_p": list_of_projects['items'],
                   "request": request,
                   "total": list_of_projects['total'],
                   "page": list_of_projects['page']})
    return templates.TemplateResponse(
        "projects.html",
        context=sample
    )



@router.get("/{user_id}/project-upload/{project_id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project_upload(request: Request,
            user_id: int,
            project_id: int
):
    sample = rpos_context.get_context_upload_project(words.read_api_prev_url(), user_id)
    sample.update({"USER_ID": user_id, "PROJ_ID": project_id, "request": request})
    return templates.TemplateResponse(
        "upload.html",
        context=sample
    )


@router.post("/{user_id}/project-upload/{project_id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project_upload(request: Request,
        user_id: int,
        project_id: int,
        db: Session = Depends(deps.get_db),
        file: UploadFile = File(...),
        p: ProjectFinal = Depends()
):
    proj_sample = crud.project.get(db=db, id=project_id)
    p = row2dict(row=proj_sample, p=p)
    directory = os.getcwd() + f"/statics/projects/users_projects/{proj_sample.project_offer_id}"
    if proj_sample.is_taken and not proj_sample.is_pay and not proj_sample.is_finish:
        p.project_owner_id = user_id
        p.is_taken = True
        if not os.path.exists(directory):
            os.mkdir(directory)
        # if len(os.listdir(directory)) != 0:
        #     for f in os.listdir(directory):
        #         os.remove(os.path.join(directory, f))
        p.address_of_project_uploaded = handle_uploaded_file_project(f=file.file, dir=directory, name=file.filename, id_dir=proj_sample.project_offer_id)
        p.is_finish = True
        crud.project.finish_project(db=db, id=project_id, db_obj=proj_sample, obj_in=p)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some thing wrong !"
        )
    sample = rpos_context.get_context_upload_project(words.read_api_prev_url(), user_id)
    sample.update({"USER_ID": user_id, "PROJ_ID": project_id, "request": request})
    return templates.TemplateResponse(
        "upload.html",
        context=sample
    )


@router.get("/{user_id}/project-finish/{project_id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project_upload(request: Request,
            user_id: int,
            project_id: int
):
    sample = rpos_context.get_context_accept_project(words.read_api_prev_url(), user_id)
    sample.update({"url_download_proj": "/api/v1/users/"+str(user_id)+"/project-download/"+str(project_id), "USER_ID": user_id, "PROJ_ID": project_id, "request": request})
    return templates.TemplateResponse(
        "accept_project.html",
        context=sample
    )



@router.post("/{user_id}/project-finish/{project_id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project_upload(request: Request,
            user_id: int,
            project_id: int,
            db: Session = Depends(deps.get_db),
            common: Optional[int] = Form(...),
            common_des: Optional[str] = Form(...),
            p: ProjectFinal = Depends()
):
    proj_sample = crud.project.get(db=db, id=project_id)
    p = row2dict(row=proj_sample, p=p)
    if proj_sample.is_taken and proj_sample.is_finish and not proj_sample.is_pay and common >=0 and common <= 5:
        user_payer = crud.user.get(db=db, id=user_id)
        user_receiver = crud.user.get(db=db, id=proj_sample.project_owner_id)
        res = ombre.check_wallet(username=user_payer.username_omb, password=user_payer.password_omb)
        if float(res["balance"]) > proj_sample.cost:
            res = ombre.transfer(from_user=user_payer.username_omb, from_pass=user_payer.password_omb, to_user=user_receiver.username_omb, to_pass=user_receiver.password_omb, amount=int(proj_sample.cost))
            print(res)
            p.common = common
            p.common_describe = common_des
            p.is_pay = True
            p.end_date = datetime.datetime.today().now()
            crud.project.finish_project(db=db, db_obj=proj_sample, obj_in=p, id=project_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Balance is not enough !!!",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something is wrong !",
        )
    sample = rpos_context.get_context_accept_project(words.read_api_prev_url(), user_id)
    sample.update({"url_download_proj": "/api/v1/users/"+str(user_id)+"/project-download/"+str(project_id), "USER_ID": user_id, "PROJ_ID": project_id,
                   "request": request})
    return templates.TemplateResponse(
        "accept_project.html",
        context=sample
    )


@router.get("/{user_id}/project-download/{project_id}", response_class=FileResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(deps.get_current_active_user)])
def project_upload(
            user_id: int,
            project_id: int,
            db: Session = Depends(deps.get_db)
):
    sample = crud.project.get(db=db, id=project_id)
    if sample.project_offer_id == user_id and sample.is_finish:
        return FileResponse(path=sample.address_of_project_uploaded)
    return None
