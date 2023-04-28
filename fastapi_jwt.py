import os
import uvicorn
from fastapi import FastAPI, status, Response, security, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)
# logging.disable()  # uncomment this for deployment or change aboce to CRITICAL or ERROR
logger = logging.getLogger(__name__)

try:  # for testing
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
except KeyError:  # for deployment implement env variables
    pass
# END
USERNAME = os.environ["USER"]
SECRET = os.environ["SECRET"]
PASSWRD = os.environ["PASSWORD"]


app = FastAPI(redoc_url=None)


http_basic = security.HTTPBasic()


class User(BaseModel):
    username: str
    password: str


class BasicInput(BaseModel):
    firstname: str
    lastname: str
    age: int
    email: str


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET


@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt

# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     if "has expired " in exc.message:
#         pass
#     elif "timeout" in exc.message:
#         pass
#     else:
#         return JSONResponse(status_code=exc.status_code, content={"return": exc.message})


@app.post('/login')
async def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != USERNAME or user.password != PASSWRD:
        raise HTTPException(status_code=401, detail="Bad username or password")
        # subject identifier for whom this token is, for example id or username from database
    # if authentication is OK, then proceed with creating a new token. Tweak the expiration time.
    access_token = Authorize.create_access_token(subject=user.username, expires_time=timedelta(minutes=15))
    return {"access_token": access_token}


@app.post("/get_user_info")
async def get_user_info(userinput: BasicInput, response: Response, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    if "@" not in userinput.email:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f'{userinput.email} is not a proper mail format.'}
    else:
        print("this")
        response.status_code = status.HTTP_202_ACCEPTED
        return {"full_name": userinput.firstname + " " + userinput.lastname, "email": userinput.email}


"""get method, does not expect any input, but returns whatever is programmed to do. Sets status 202"""


@app.get("/get_message")
async def get_message(response: Response, authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        print('here')
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "This is the message you were waiting for."}
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")


if __name__ == '__main__':
    uvicorn.run("fastapi_jwt:app", port=8080, reload=True)
