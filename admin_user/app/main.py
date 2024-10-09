from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routers import admin_user
from app.config.database import engine, Base
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI(docs_url="/docsadmin_user",openapi_url="/docsadmin_user.json",redoc_url=None)
#app = FastAPI()

# Configurar la información de la aplicación
app.title = "admin User Service"
app.version = "0.0.2"
app.description = "api for aquashield admin user microservice"
app.docs_url = "/"

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "access-control-allow-methods", "access-control-allow-origin", "authorization", "content-type"],
)

# @app.get("/")
# async def root():
#     return {"message": "Aquashield_backend_dev_admin_user_service"}


# Incluir los routers de las rutas
app.include_router(admin_user.router)

handler = Mangum(app)

