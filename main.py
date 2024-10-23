from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
CURRENCY_LIST = ["USD", "EUR", "GBP", "JPY", "RUB"]


@app.get("/convert/")
async def convert_currency(amount: float, from_currency: str, to_currency: str):
    if from_currency not in CURRENCY_LIST or to_currency not in CURRENCY_LIST:
        raise HTTPException(status_code=400, detail="Unsupported currency")

    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching currency data")

        data = response.json()
        rates = data.get("rates")

        if from_currency not in rates or to_currency not in rates:
            raise HTTPException(status_code=400, detail="Currency not found in the rates")

        converted_amount = (amount / rates[from_currency]) * rates[to_currency]
        return {
            "result": round(converted_amount, 2)
        }
