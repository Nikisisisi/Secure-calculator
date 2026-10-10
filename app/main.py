import math
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


VERSION_FILE = Path(__file__).parent.parent / "VERSION"


def get_version():
    return VERSION_FILE.read_text(encoding="utf-8").strip()


APP_VERSION = get_version()


app = FastAPI(
    title="Secure Calculator API",
    description="API-калькулятор для учебной работы по безопасной разработке",
    version=APP_VERSION,
)


BAD_REQUEST_RESPONSES = {
    400: {
        "description": "Bad request or malformed JSON body"
    }
}


class CalculationRequest(BaseModel):
    a: float = Field(
        ge=-1_000_000,
        le=1_000_000,
        allow_inf_nan=False
    )

    b: float = Field(
        ge=-1_000_000,
        le=1_000_000,
        allow_inf_nan=False
    )

    @field_validator("a", "b", mode="before")
    @classmethod
    def reject_boolean_values(cls, value):
        if isinstance(value, bool):
            raise ValueError("Boolean values are not allowed")
        return value


class DivideRequest(CalculationRequest):
    b: float = Field(
        ge=-1_000_000,
        le=1_000_000,
        allow_inf_nan=False,
        json_schema_extra={
            "anyOf": [
                {"maximum": -1e-300},
                {"minimum": 1e-300}
            ]
        }
    )

    @field_validator("b")
    @classmethod
    def reject_unsafe_divisor(cls, value):
        if abs(value) < 1e-300:
            raise ValueError(
                "Divisor magnitude must be at least 1e-300"
            )
        return value


class PowerRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "not": {
                "properties": {
                    "a": {"const": 0},
                    "b": {"maximum": -1}
                },
                "required": ["a", "b"]
            }
        }
    )

    a: float = Field(
        ge=-1_000_000,
        le=1_000_000,
        allow_inf_nan=False
    )

    b: int = Field(
        ge=-20,
        le=20
    )

    @field_validator("a", "b", mode="before")
    @classmethod
    def reject_boolean_values(cls, value):
        if isinstance(value, bool):
            raise ValueError("Boolean values are not allowed")
        return value


class FactorialRequest(BaseModel):
    n: int = Field(
        ge=0,
        le=100
    )

    @field_validator("n", mode="before")
    @classmethod
    def reject_invalid_integer_types(cls, value):
        if isinstance(value, bool):
            raise ValueError("Boolean values are not allowed")

        if not isinstance(value, (int, float)):
            raise ValueError("Only numeric integer values are allowed")

        return value

@app.get("/")
def root():
    return {
        "message": "Secure Calculator API is running",
        "version": APP_VERSION
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/web", response_class=HTMLResponse)
def web_interface():
    html_file = Path(__file__).parent / "index.html"
    return FileResponse(html_file)


@app.post(
    "/calculate/add",
    responses=BAD_REQUEST_RESPONSES
)
def add(data: CalculationRequest):
    return {"result": data.a + data.b}


@app.post(
    "/calculate/subtract",
    responses=BAD_REQUEST_RESPONSES
)
def subtract(data: CalculationRequest):
    return {"result": data.a - data.b}


@app.post(
    "/calculate/multiply",
    responses=BAD_REQUEST_RESPONSES
)
def multiply(data: CalculationRequest):
    return {"result": data.a * data.b}


@app.post(
    "/calculate/divide",
    responses=BAD_REQUEST_RESPONSES
)
def divide(data: DivideRequest):
    if data.b == 0:
        raise HTTPException(
            status_code=400,
            detail="Division by zero is not allowed"
        )

    result = data.a / data.b

    if not math.isfinite(result):
        raise HTTPException(
            status_code=400,
            detail="Division result is outside the supported numeric range"
        )

    return {"result": result}


@app.post(
    "/calculate/power",
    responses=BAD_REQUEST_RESPONSES
)
def power(data: PowerRequest):
    if data.a == 0 and data.b < 0:
        raise HTTPException(
            status_code=400,
            detail="Zero cannot be raised to a negative power"
        )

    try:
        result = data.a ** data.b
    except OverflowError:
        raise HTTPException(
            status_code=400,
            detail="Power result is outside the supported numeric range"
        )

    return {"result": result}



@app.post(
    "/calculate/factorial",
    responses=BAD_REQUEST_RESPONSES
)
def factorial(data: FactorialRequest):
    result = 1

    for number in range(2, data.n + 1):
        result *= number

    return {"result": result}