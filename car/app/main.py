from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routers import car
from app.config.database import engine, Base
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
#app = FastAPI(root_path="/dev",docs_url="/docscar",openapi_url="/docscar.json",redoc_url=None)
app = FastAPI()

# Configurar la información de la aplicación
app.title = "Car Service"
app.version = "0.0.1"
app.description = "api for aquashield Car service"
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
     return {"message": "Aquashield_backend_dev_car_service"} """


# Incluir los routers de las rutas
app.include_router(car.router)

handler = Mangum(app)

