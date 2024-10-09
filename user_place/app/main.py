from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routers import user_place
from app.config.database import engine, Base
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI(docs_url="/docsuser_place",openapi_url="/docsuser_place.json",redoc_url=None)
#app = FastAPI()

# Configurar la información de la aplicación
app.title = "User_Place Service"
app.version = "0.0.1"
app.description = "api for aquashielduser_place service"
app.docs_url = "/"


# Definir orígenes permitidos
origins = [
    "http://127.0.0.1:5500",  # Tu frontend local
    "http://localhost:5500",  # Opción adicional para localhost
    "*"
]

# Agregar middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "access-control-allow-methods", "access-control-allow-origin", "authorization", "content-type"],
)

""" @app.get("/")
async def root():
     return {"message": "Aquashield_backend_dev_owner_service"} """


# Incluir los routers de las rutas
app.include_router(user_place.router)

handler = Mangum(app)

