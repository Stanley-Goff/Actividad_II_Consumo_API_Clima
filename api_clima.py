import requests

CIUDADES = {
    "Tegucigalpa": (14.0723, -87.1921),
    "San Pedro Sula": (15.5042, -88.0250),
    "La Ceiba": (15.7597, -86.7822),
    "Choluteca": (13.3000, -87.1900),
    "Comayagua": (14.4600, -87.6500),
    "Berlin": (52.52, 13.41)
}


def consumir_api_clima(latitud, longitud):

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitud}"
        f"&longitude={longitud}"
        f"&current=temperature_2m,wind_speed_10m"
        f"&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    respuesta = requests.get(url, timeout=10)

    if respuesta.status_code == 200:
        return respuesta.json()

    return None