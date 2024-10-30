# cc2024_crashy


## Data Sets

The data sets can be fetched from kaggle using the following python lines:

```python
import kagglehub

path = kagglehub.dataset_download("humansintheloop/car-parts-and-car-damages")
print("Path to dataset files:", path)

path = kagglehub.dataset_download("hendrichscullen/vehide-dataset-automatic-vehicle-damage-detection")
print("Path to dataset files:", path)
```

Typically they are cached under ~/.cache/kagglehub/

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
