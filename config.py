from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./Registers.db"
database_file = "./Registers.db"

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    plataforma = Column(String, index=True)
    usuario = Column(String, index=True)
    senha = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, plataforma={self.plataforma}, usuario={self.usuario}, senha={self.senha})>"

# Criar tabela de usuários no banco de dados, se não existir
# Verificar se o banco de dados já existe
if not os.path.exists(database_file):
    # Criar tabela de usuários no banco de dados, se não existir
    Base.metadata.create_all(bind=engine)
    print("Banco de dados criado.")
else:
    print("Banco de dados já existe.")


