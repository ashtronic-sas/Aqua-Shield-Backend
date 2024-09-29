from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routers import user
from app.config.database import engine, Base
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI(root_path="/dev",docs_url="/docsuser",openapi_url="/docsuser.json",redoc_url=None)
#app = FastAPI()

# Configurar la información de la aplicación
app.title = "User Service"
app.version = "0.0.2"
app.description = "api for aquashield user microservice"
app.docs_url = "/"


# Definir orígenes permitidos
origins = [
    "http://127.0.0.1:5500",  # Tu frontend local
    "http://localhost:5500"   # Opción adicional para localhost
]

# Agregar middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir los orígenes definidos
    allow_credentials=True,  # Permitir el uso de cookies o credenciales
    allow_methods=["*"],     # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],     # Permitir todos los encabezados
)

@app.get("/")
async def root():
     return {"message": "Aquashield_backend_dev_user_service"}


# Incluir los routers de las rutas
app.include_router(user.router)

handler = Mangum(app)

