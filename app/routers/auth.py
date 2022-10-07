from typing import Optional
from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse
from models import User
from passlib.context import CryptContext
from starlette.responses import RedirectResponse
from datetime import datetime, timedelta
from jose import jwt, JWTError
from utils.schemas import LoginForm
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from . import templates

# [Authorization and authentication]

SECRET_KEY = '3K75JD2JKDS99U342YINQ0'

ALGORITHM = "HS256"

by_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)

oatuh2_bearer = OAuth2PasswordBearer(tokenUrl='token')


def hash_password(password):
    return by_crypt_context.hash(password)


def verfiy_password(password, hashed_password):
    return by_crypt_context.verify(password, hashed_password)


def authenticate_user(username: str, password: str):
    user = User.get(username).dict()
    if not user:
        return False
    if not verfiy_password(password, user['password']):
        return False

    return user

# [Creating access token]


def create_access_token(username: str,
                        user_pk: str,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "pk": user_pk}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode['exp'] = expire
    # [Encoding JWT]
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# [Check is current user has a valid access token]


async def get_current_user(request: Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None
        # [Decoding JWT]
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_pk: str = payload.get('pk')
        if username is None or user_pk is None:
            return False

        return {"username": username, "pk": user_pk}

    except JWTError:
        return HTTPException(status_code=404, detail="Not found")

# [Login logic for setting access token as cookie]


@router.post('/token')
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return False
    # [Setting token expiration to 1 hour]
    token_expires = timedelta(minutes=60)
    access_token = create_access_token(user['username'],
                                       user['pk'],
                                       expires_delta=token_expires)
    # [Setting JWT as cookie]
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return True


@router.get('/', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/', response_class=HTMLResponse)
async def login(request: Request):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(
            url="/orders", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get('/logout')
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")

    return response
