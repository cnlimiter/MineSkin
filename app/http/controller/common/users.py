from datetime import timedelta

from fastapi import APIRouter, Depends, Security, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.Exception import LoginError
from app.core.Deps import get_db, get_current_user
from app.core.Auth import authenticate_user
from app.models.user import User
from app.schemas.auth import LoginToken
from app.core.Auth import create_access_token
from config.jwt import settings as JWTConfig

router = APIRouter(
)


@router.get("/")
async def root():
    return "Welcome!"


@router.post("/login", response_model=LoginToken, dependencies=[Depends(get_db)])
def me(auth_user: OAuth2PasswordRequestForm = Depends()):
    """
    登录
    """

    user = authenticate_user(auth_user.username, auth_user.password)
    if not user:
        raise LoginError("用户不存在或密码错误")
    access_token_expires = timedelta(minutes=JWTConfig.TTL)
    return LoginToken(
        access_token=create_access_token(user.user_id, expires_delta=access_token_expires),
        token_type="bearer"
    )


@router.get('/login/getinfo', dependencies=[Depends(get_db)])
def login_getinfo(
        current_user: User = Depends(get_current_user)
):
    data = {
        'username': current_user.username,
        'roles': ['admin', ]
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


# @router.put("/avatar/upload", dependencies=[Security(check_permissions)], summary="头像修改")
# async def avatar_upload(req: Request, avatar: UploadFile = File(...)):
#     """
#     头像上传
#     :param req:
#     :param avatar:
#     :return:
#     """
#     # 文件存储路径
#     path = f"{settings.STATIC_DIR}/upload/avatar"
#     start = time.time()
#     filename = random_str() + '.' + avatar.filename.split(".")[1]
#     try:
#         if not os.path.isdir(path):
#             os.makedirs(path, 0o777)
#         res = await avatar.read()
#         with open(f"{path}/{filename}", "wb") as f:
#             f.write(res)
#         await User.filter(id=req.state.user_id).update(header_img=f"/upload/avatar/{filename}")
#         data = {
#             'time': time.time() - start,
#             'url': f"/upload/avatar/{filename}"}
#         return success(msg="更新头像成功", data=data)
#     except Exception as e:
#         print("头像上传失败:", e)
#         return fail(msg=f"{avatar.filename}上传失败!")