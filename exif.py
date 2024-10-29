"""Module to analyze EXIF data."""

from io import BytesIO

import exifread
from exifread.classes import IfdTag
from exifread.utils import get_gps_coords


class ExifData:
    """Class to handle EXIF data."""

    images_tags: list[dict[str, IfdTag]] = []

    def __init__(self, images: list[bytes]) -> None:
        """Intiialize the by parisng the images."""
        self.images_tags = [
            exifread.process_file(BytesIO(image), details=False) for image in images
        ]

    @property
    def locations(self) -> list[tuple[float, float]]:
        """Get a list of locations."""
        return [get_gps_coords(tags) for tags in self.images_tags]

    @property
    def creation_times(self) -> list[str]:
        """Get a list of locations."""
        return [
            tags["EXIF DateTimeOriginal"].values  # noqa: PD011
            if "EXIF DateTimeOriginal" in tags
            else ""
            for tags in self.images_tags
        ]
