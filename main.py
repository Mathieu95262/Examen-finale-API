from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

# GET /ping
@app.get("/ping")
def ping():
    return "pong"

class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    id: str
    brand: str
    model: str
    characteristics: Characteristic

cars_db: List[Car] = [
    Car(
        id="1",
        brand="Wolswagen",
        model="Mk4",
        characteristics=Characteristic(max_speed=200, max_fuel_capacity=70)
    ),
    Car(
        id="2",
        brand="BMW",
        model="E36",
        characteristics=Characteristic(max_speed=250, max_fuel_capacity=100)
    )
]

# POST /cars
@app.post("/cars", status_code=status.HTTP_201_CREATED)
def create_cars(new_cars: List[Car]):
    cars_db.extend(new_cars)
    return new_cars

# GET /cars
@app.get("/cars")
def get_cars():
    return cars_db

# GET /cars/{id}
@app.get("/cars/{id}")
def get_car(id: str):
    for car in cars_db:
        if car.id == id:
            return car
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"La voiture avec l'identifiant '{id}' n'existe pas ou n'a pas été trouvée."
    )