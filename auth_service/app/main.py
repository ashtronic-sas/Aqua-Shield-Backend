from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routes import auth
from app.utils.database import engine, Base

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI()

# Incluir los routers de las rutas
app.include_router(auth.router)



