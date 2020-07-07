# CO2 Demo App

### To do
- receive cart.csv through API (will use fast-api package)
- add carbon footprint for product category
- add store location for transportation from next hub

## Running
- run directly with `streamlit run app.py`
- interact at `localhost:8501`

### Run with Docker
- Pull the container `docker pull bjoern13/co2:latest`
- or build locally with ` docker build --pull --rm -f "DOCKERFILE" -t co2:latest "."`
- run with `docker run -p 8501:8501 co2:latest`