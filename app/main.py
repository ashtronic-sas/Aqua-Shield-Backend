from fastapi import FastAPI
from mangum import Mangum
import requests

app = FastAPI()

@app.get('/')
async def index():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    return data

handler = Mangum(app)
