from pydantic import BaseModel, constr

class UserRegister(BaseModel):
  username: str
  password: str
  role: str