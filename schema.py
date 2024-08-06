from pydantic import BaseModel
# 
# 
# Modelo Pydantic para validação
class UserCreate(BaseModel):
    plataforma: str
    usuario: str
    senha: str
