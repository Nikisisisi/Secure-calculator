from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


app = FastAPI(
    title="Secure Calculator API",
    description="API-калькулятор для учебной работы по безопасной разработке",
    version="1.0.0",
)


class CalculationRequest(BaseModel):
    a: float
    b: float


@app.get("/")
def root():
    return {
        "message": "Secure Calculator API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/web")
def web_interface():
    html_file = Path(__file__).parent / "index.html"
    return FileResponse(html_file)


@app.post("/calculate/add")
def add(data: CalculationRequest):
    return {"result": data.a + data.b}


@app.post("/calculate/subtract")
def subtract(data: CalculationRequest):
    return {"result": data.a - data.b}


@app.post("/calculate/multiply")
def multiply(data: CalculationRequest):
    return {"result": data.a * data.b}


@app.post("/calculate/divide")
def divide(data: CalculationRequest):
    if data.b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed"
        )

    return {"result": data.a / data.b}