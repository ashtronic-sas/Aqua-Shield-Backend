from fastapi import FastAPI
from app.routes import order
from mangum import Mangum

app = FastAPI()

app.include_router(order.router)

handler = Mangum(app)

