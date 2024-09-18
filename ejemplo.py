import requests

# mostremos información del dolar versus el peso en apis gratuitas
response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
data = response.json()
print(data)
