import streamlit as st
import pandas as pd

# URL del archivo raw en GitHub
url_github = 'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos.json'

# Cargar los datos desde GitHub
try:
    df = pd.read_json(url_github)
    st.success('Datos cargados correctamente desde GitHub.')
except Exception as e:
    st.error(f'Error al cargar los datos: {e}')
    st.stop()

# Título de la aplicación
st.title('🔎 Buscador de videos de YouTube')
st.markdown('---')

# Campo de búsqueda
busqueda = st.text_input('Escribe lo que quieres buscar en los videos:', '')

# Lógica de búsqueda mejorada
if busqueda:
    # Convertir la búsqueda a minúsculas y dividir por espacios
    palabras_busqueda = busqueda.lower().split()

    # Iniciar un filtro que será True para todos los videos
    filtro_general = pd.Series([True] * len(df), index=df.index)

    # Iterar sobre cada palabra para construir el filtro
    for palabra in palabras_busqueda:
        # El filtro se actualiza con una condición 'Y' (&)
        # para asegurar que todas las palabras estén presentes
        filtro_general &= (
            #df['resumen'].str.lower().str.contains(palabra, na=False) |
            df['transcripcion'].str.lower().str.contains(palabra, na=False)
        )

    # Aplicar el filtro al DataFrame
    resultados = df[filtro_general]

    if not resultados.empty:
        st.subheader(f'Videos que contienen todas las palabras de "{busqueda}":')
        # Mostrar los resultados
        for index, row in resultados.iterrows():
            st.write(f"**Título:** {row['titulo']}")
            st.write(f"**Enlace:** [Ver video]({row['enlace']})")
            st.markdown('---')
    else:
        st.info('No se encontraron videos con ese contenido.')




