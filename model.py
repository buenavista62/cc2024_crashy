"""Module with the response models."""

from enum import Enum

from pydantic import BaseModel, Field


class DamageSeverity(str, Enum):
    """
    DamageSeverity is an enumeration representing different levels of damage severity.

    Attributes:
        low (str): Represents low severity damage, labeled as "tief".
        medium (str): Represents medium severity damage, labeled as "mittel".
        high (str): Represents high severity damage, labeled as "hoch".

    """

    low = "tief"
    medium = "mittel"
    high = "hoch"


class DamageLocation(str, Enum):
    """
    An enumeration representing different locations of damage on vehicle.

    Attributes:
            front (str): Represents damage to the front of the vehicle.
            rear (str): Represents damage to the rear of the vehicle.
            sides (str): Represents damage to the sides of the vehicle.
            roof (str): Represents damage to the roof of the vehicle.

    """

    front = "Front"
    rear = "Heck"
    sides = "Seiten"
    roof = "Dach"


class VehicleDamage(BaseModel):
    """
    VehicleDamage model representing the damage details of a vehicle.

    Attributes:
        fire_present (bool): Indicates if there are signs of fire on the vehicle.
        damage_severity (DamageSeverity): Severity of the damage.
        damage_location (list[DamageLocation]): Location of the damage on the vehicle.
        detailed_damage_description (list[str]): Detailed description of the visible
        damages.

    """

    fire_present: bool = Field(
        ..., description="Indicates if there are signs of fire on the vehicle."
    )
    damage_severity: DamageSeverity = Field(..., description="Severity of the damage.")
    damage_location: list[DamageLocation] = Field(
        ..., description="Location of the damage on the vehicle."
    )
    detailed_damage_description: list[str] = Field(
        ..., description="Detailed description of the visible damages."
    )


class DamageReport(BaseModel):
    """An accident report model."""

    car_present: list[bool] = Field(
        ..., description="Indicates if a vehicle is fully visible in a given image."
    )
    license_plate_number: str | None = Field(
        None, description="License plate number if fully visible."
    )
    damage_recognized: bool = Field(
        ..., description="Indicates if damages are recognized on the vehicle."
    )
    damage_fully_visible: bool = Field(
        ..., description="Indicates if the damage is fully visible in the images."
    )
    vehicle_damage: VehicleDamage = Field(
        ..., description="Details of the vehicle damage."
    )
    number_of_valid_images: int = Field(
        ..., description="Number of valid images used for the evaluation."
    )
    number_of_unique_vehicles: int = Field(
        ..., description="Number of unique vehicles visible in the images."
    )
