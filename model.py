"""Module with the response models."""

from pydantic import BaseModel, Field


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

    number_of_valid_images: int = Field(
        ..., description="Number of valid images used for the evaluation."
    )
    number_of_unique_vehicles: int = Field(
        ..., description="Number of unique vehicles visible in the images."
    )

    is_fire_present: bool = Field(
        ..., description="Indicates if there are signs of fire."
    )

    is_glass_damage_present: bool = Field(
        ..., description="Indicates if there are signs of glass damage."
    )

    frontscheibe_glass_damage: bool | None = Field(
        None,
        description="Indicates if there is glass damage on the front windshield.",
        depends_on="is_glass_damage_present",
    )
    heckscheibe_glass_damage: bool | None = Field(
        None,
        description="Indicates if there is glass damage on the rear windshield.",
        depends_on="is_glass_damage_present",
    )
    seitenscheibe_glass_damage: bool | None = Field(
        None,
        description="Indicates if there is glass damage on the side windows.",
        depends_on="is_glass_damage_present",
    )
    dach_panoramafenster_glass_damage: bool | None = Field(
        None,
        description="Indicates if there is glass damage on the roof or panoramic "
        "windows.",
        depends_on="is_glass_damage_present",
    )
    detailed_damage_description: list[str] = Field(
        ..., description="Detailed description of the visible damages."
    )
    is_collision: bool = Field(
        ..., description="Indicates if there are signs of a collision."
    )
    collision_with_object: bool | None = Field(
        None,
        description="Indicates if there is a collision with an object.",
        depends_on="is_collision",
    )
    collision_with_car: bool | None = Field(
        None,
        description="Indicates if there is a collision with another car.",
        depends_on="is_collision",
    )
    collision_with_animal: bool | None = Field(
        None,
        description="Indicates if there is a collision with an animal.",
        depends_on="is_collision",
    )
    collision_other: bool | None = Field(
        None,
        description="Indicates if there is a collision with another object.",
        depends_on="is_collision",
    )
    is_vandalism: bool = Field(
        ..., description="Indicates if there are signs of vandalism."
    )
    is_theft: bool = Field(
        ..., description="Indicates if there are signs of theft."
    )
    is_potential_hail_damage: bool = Field(
        ..., description="Indicates if there are signs of potential hail damage."
    )
    is_potential_storm_damage: bool = Field(
        ..., description="Indicates if there are signs of potential_storm damage."
    )
    is_potential_rockfall_damage: bool = Field(
        ..., description="Indicates if there are signs of potential_rockfall damage."
    )
    is_other_damage: bool = Field(
        ..., description="Indicates if there are signs of other damage."
    )
    is_person_injured: bool = Field(
        ..., description="Indicates if a person is injured."
    )
