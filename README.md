# cc2024_crashy

## Introduction
This repository contains a streamlit application to automatically fill out damage reports. 

## Project Diagram

```mermaid
graph TD;
    A[User] -->|uploads image| B[Streamlit App]
    A[User] -->|records incident| B
    B -->|processes image| C[GPT-4o]
    B -->|processes audio| D[Whisper-2]
    D -->|translation/transcription| C
    D -->|extracts information| B
    C -->|extracts information| E[Response Model]
    E -->|fills damage report| B
    B -->|displays results| A
```

## Installlation
The python streamlit application is using uv to manage the virtual environments and the installation.

The following instructions work for Linux:
```bash
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# setup virtual env and install packages
uv sync
# run the streamlit application
uv run streamlit run crashy.py
```

## Container

Crashy can be build to run in a ccontainer.

```bash
# build the container image
docker build -t crashy .
# run the container supposing openai secret is in .secret-openai
docker run --rm -e OPENAI_API_KEY=$$(cat .secret-openai) -p 8501:8501 crashy
# open the browser to interact with crashy
open http://localhost:8501
```

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
