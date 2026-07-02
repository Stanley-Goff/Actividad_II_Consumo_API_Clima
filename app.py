import streamlit as st
import pandas as pd

from api_clima import consumir_api_clima
from api_clima import CIUDADES

from database import (
    crear_tabla,
    guardar_consulta,
    consultar_datos,
    eliminar_datos
)

st.set_page_config(
    page_title="Clima API",
    page_icon="🌤️",
    layout="wide"
)

crear_tabla()

st.title("🌤️ Consumo de API Meteorológica")

menu = st.sidebar.selectbox(

    "Seleccione una opción",

    [

        "Inicio",
        "Consultar clima",
        "Historial",
        "Eliminar historial"

    ]

)

if menu == "Inicio":

    st.header("Bienvenido")

    st.write(
        """
        Consulta información meteorológica mediante la API pública
        Open-Meteo y almacena las consultas realizadas.
        """
    )

elif menu == "Consultar clima":

    ciudad = st.selectbox(

        "Seleccione una ciudad",

        list(CIUDADES.keys())

    )

    latitud, longitud = CIUDADES[ciudad]

    if st.button("Consultar clima"):

        datos = consumir_api_clima(latitud, longitud)

        if datos:

            actual = datos["current"]

            temperatura = actual["temperature_2m"]
            viento = actual["wind_speed_10m"]

            guardar_consulta(ciudad, temperatura, viento)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Temperatura actual",
                    f"{temperatura} °C"
                )

            with col2:
                st.metric(
                    "Velocidad del viento",
                    f"{viento} km/h"
                )

            hourly = datos["hourly"]

            df = pd.DataFrame({

                "Hora": pd.to_datetime(hourly["time"]),
                "Temperatura": hourly["temperature_2m"],
                "Humedad": hourly["relative_humidity_2m"],
                "Viento": hourly["wind_speed_10m"]

            })

            st.subheader("Datos horarios")

            st.dataframe(df, use_container_width=True)

            st.subheader("Temperatura")

            st.line_chart(
                df.set_index("Hora")["Temperatura"]
            )

            st.subheader("Humedad")

            st.line_chart(
                df.set_index("Hora")["Humedad"]
            )

            st.subheader("Velocidad del viento")

            st.line_chart(
                df.set_index("Hora")["Viento"]
            )

        else:

            st.error("No fue posible obtener los datos.")

elif menu == "Historial":

    datos = consultar_datos()

    if datos:

        df = pd.DataFrame(

            datos,

            columns=[

                "ID",
                "Ciudad",
                "Temperatura",
                "Viento"

            ]

        )

        st.dataframe(df, use_container_width=True)

    else:

        st.info("No existen registros.")

elif menu == "Eliminar historial":

    if st.button("Eliminar"):

        eliminar_datos()

        st.success("Historial eliminado correctamente.")