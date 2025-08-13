import streamlit as st
import pandas as pd

# URLs de los archivos JSON fragmentados en GitHub
urls_github = [
    'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos_parte_1.json',
    'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos_parte_2.json'
    # Puedes añadir más archivos si lo necesitas, por ejemplo:
    # 'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos_parte_3.json'
]

# Título de la aplicación
st.title('🖤 Buscador Clave Geo 🏴‍☠️')
st.markdown('---')

# Cargar los datos desde GitHub
dataframes = []
error_loading = False
loading_message = st.info('Surcando los mares.')

try:
    for url in urls_github:
        df_temp = pd.read_json(url)
        dataframes.append(df_temp)
    
    # Combinar todos los DataFrames en uno solo
    df = pd.concat(dataframes, ignore_index=True)
    loading_message.success('Datos cargados y combinados correctamente desde GitHub.')
    
except Exception as e:
    loading_message.error(f'Error al cargar los datos: {e}')
    error_loading = True

if error_loading:
    st.stop()

# --- Manejo de la columna 'enlace' ---
# Si la columna 'enlace' no existe en absoluto, detenemos la app
if 'enlace' not in df.columns:
    st.error('Error: La columna "enlace" no se encuentra en el archivo JSON. Por favor, revisa el archivo en GitHub.')
    st.stop()
# -------------------------------------

# Campo de búsqueda
busqueda = st.text_input('Escribe palabras clave a buscar en los videos:', '')

# Lógica de búsqueda mejorada
if busqueda:
    palabras_busqueda = busqueda.lower().split()
    filtro_general = pd.Series([True] * len(df), index=df.index)

    # Prevenir KeyError si las columnas no existen
    if 'transcripcion' in df.columns:
        for palabra in palabras_busqueda:
            filtro_general &= (
                df['transcripcion'].str.lower().str.contains(palabra, na=False)
            )
    else:
        st.warning('La columna "transcripcion" no existe para realizar la búsqueda.')
        resultados = pd.DataFrame() # DataFrame vacío

    if 'transcripcion' in df.columns:
        resultados = df[filtro_general]
    else:
        resultados = pd.DataFrame()

    if not resultados.empty:
        st.subheader(f'Videos que contienen todas las palabras de "{busqueda}":')
        # Mostrar los resultados
        for index, row in resultados.iterrows():
            # Añado una verificación para asegurar que la clave 'enlace' exista en esta fila
            if 'enlace' in row and 'titulo' in row:
                st.write(f"**Título:** {row['titulo']}")
                st.write(f"**Enlace:** [Ver video]({row['enlace']})")
                st.markdown('---')
            else:
                st.warning(f"Se encontró un resultado sin la información completa en el índice: {index}")
                st.markdown('---')
    else:
        st.info('No se encontraron videos con ese contenido.')





