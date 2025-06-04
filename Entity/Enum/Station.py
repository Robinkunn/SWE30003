from enum import Enum

class Station(Enum):
    UNIMAS = "UNIMAS"
    CITY_ONE = "City One"
    PENDING = "Pending"
    THE_SPRING = "The Spring"
    WATERFRONT = "Waterfront"
    SWINBURNE = "Swinburne"

    @classmethod
    def list_stations(cls):
        return list(cls)
