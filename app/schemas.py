from pydantic import BaseModel
from datetime import date

class HouseFeatures(BaseModel):
    transaction_date: date
    house_age: float
    distance_to_the_nearest_MRT_station: float
    number_of_convenience_stores: int
    latitude: float
    longitude: float