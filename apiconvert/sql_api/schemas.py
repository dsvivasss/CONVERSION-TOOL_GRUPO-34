from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    username: str
    password: str
    email: str  

class User(UserBase):
    id: int
    class Config:
        orm_mode = True


class FileBase(BaseModel):
    fileName: str
    newFormat: str
    oldFormat: str
    status: str
    pathName: str
    timeStamp: datetime.datetime

class File(FileBase):
    id: int
    class Config:
        orm_mode = True