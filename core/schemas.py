from pydantic import BaseModel

# user
class UserLoginBody(BaseModel):
    username: str = "otaw"
    password: str = "123"
class UserRegisterBody(BaseModel):
    username: str = "otaw"
    password: str = "123"
class UserUpdateBody(BaseModel):
    username:     str = "otaw"
    password:     str = "123"
    new_username: str
    new_password: str

# test
class TestAddBody(BaseModel):
    title: str
class TestUpdateBody(BaseModel):
    id:    int
    title: str
