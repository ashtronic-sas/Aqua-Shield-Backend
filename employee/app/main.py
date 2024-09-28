from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routers import employee
from app.config.database import engine, Base
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Instanciar la aplicación de FastAPI
app = FastAPI(root_path="/dev",docs_url="/docsemployee",openapi_url="/docsemployee.json",redoc_url=None)
#app = FastAPI()

# Configurar la información de la aplicación 
app.title = "employee service"
app.version = "0.0.1"
app.description = "api for aquashield employee service microservice"
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
    return {"message": "Aquashield backend employee service"}


# Incluir los routers de las rutas
app.include_router(employee.router)

handler = Mangum(app)