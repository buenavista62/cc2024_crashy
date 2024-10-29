# cc2024_crashy


## Manipulate exif data
Images may have embedded  [EXIF metadata](https://en.wikipedia.org/wiki/Exif). They data can be displayed:

```bash
exiftool <path_to_image>
```
... and manipulated
```bash
# manipulate picture creation time
exiftool -DateTimeOriginal="2020:01:01 06:06:06+01:00" <path_to_image>
# manipulate geolocation
exiftool -GPSLatitude*=47.54943851265131 -GPSLongitude*=7.593584082607474 -GPSAltitude*=277 <path_to_image>
```
