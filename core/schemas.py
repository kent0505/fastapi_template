from pydantic import BaseModel

# user
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

# product
class ProductAddBody(BaseModel):
    title: str
    price: int
    iid:   int
    cid:   int
class ProductUpdateBody(BaseModel):
    id:    int
    title: str
    price: int
    iid:   int
    cid:   int

# order
class OrderAddBody(BaseModel):
    amount:  int = 1
    uid:     int
    pid:     int
    address: str = "41.315166, 69.243769"
    notes:   str = ""