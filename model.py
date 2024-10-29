"""Module with the response models."""

from typing import Optional

from pydantic import BaseModel


class AccidentReport(BaseModel):
    """An accident report model."""

    car_present: bool
    damage_recognized: bool
    damage_fully_visible: bool
    damage_severity: str  # 'low', 'medium', 'high'
    damage_location: str  # z.B. 'Front', 'Heck', 'Seiten', 'Dach'
    fire_present: bool
    license_plate_number: Optional[str]  # noqa: UP007
    detailed_damage_description: list[str]
    number_of_valid_images: int
    number_of_unique_vehicles: int
