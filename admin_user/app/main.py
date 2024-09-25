from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routes import admin_user
from app.config.database import engine, Base
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI(root_path="/dev")
#app = FastAPI()

# Configurar la información de la aplicación
app.title = "admin User Service"
app.version = "0.0.2"
app.description = "api for aquashield admin user microservice"
app.docs_url = "/"

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Aquashield_backend_dev_admin_user_service"}


# Incluir los routers de las rutas
app.include_router(admin_user.router)

handler = Mangum(app)

