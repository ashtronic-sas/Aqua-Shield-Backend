from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routes import user
from app.utils.database import engine, Base
from mangum import Mangum

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Aquashield_backend_dev"}

@app.get("/docs")
def read_docs():
    return {"docs": "Este es el punto de documentación de FastAPI."}

# Incluir los routers de las rutas
app.include_router(user.router)

handler = Mangum(app)

