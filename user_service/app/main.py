from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routes import user
from app.utils.database import engine, Base
from mangum import Mangum

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)


handler = Mangum(app)
