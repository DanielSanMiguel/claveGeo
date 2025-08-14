import streamlit as st
import pandas as pd

# URLs de los archivos JSON fragmentados en GitHub
urls_github = [
    # Puedes añadir más archivos si lo necesitas, por ejemplo:
    'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos_parte_1.json',
    'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos_parte_2.json',
    'https://raw.githubusercontent.com/DanielSanMiguel/claveGeo/main/videos_parte_3.json'
]

# Título de la aplicación
st.title('🖤 Buscador Clave Geo 🏴‍☠️')
st.markdown('---')

# La función de carga de datos ahora usa caché para mejorar el rendimiento
@st.cache_data
def load_data(urls):
    """
    Carga y combina los datos de múltiples URLs JSON usando caché.
    """
    dataframes = []
    for url in urls:
        try:
            df_temp = pd.read_json(url)
            dataframes.append(df_temp)
        except Exception as e:
            st.error(f'Error al cargar el archivo de la URL: {url}. Error: {e}')
    
    if dataframes:
        # Combinar todos los DataFrames en uno solo
        df = pd.concat(dataframes, ignore_index=True)
        return df
    else:
        return pd.DataFrame()

# Cargar los datos desde GitHub con un mensaje de estado
loading_message = st.info('Surcando los mares... 🏴‍☠️')

try:
    df = load_data(urls_github)
    if not df.empty:
        loading_message.success('Datos cargados y combinados correctamente desde GitHub.')
    else:
        loading_message.warning('No se encontraron datos en las URLs proporcionadas.')
        st.stop()
except Exception as e:
    loading_message.error(f'Error al cargar los datos: {e}')
    st.stop()

# --- Manejo de la columna 'enlace' ---
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

    if 'transcripcion' in df.columns:
        for palabra in palabras_busqueda:
            filtro_general &= (
                df['transcripcion'].str.lower().str.contains(palabra, na=False)
            )
    else:
        st.warning('La columna "transcripcion" no existe para realizar la búsqueda.')
        resultados = pd.DataFrame()

    if 'transcripcion' in df.columns:
        resultados = df[filtro_general]
    else:
        resultados = pd.DataFrame()

    if not resultados.empty:
        st.subheader(f'Videos que contienen todas las palabras de "{busqueda}":')
        # Mostrar los resultados
        for index, row in resultados.iterrows():
            if 'enlace' in row and 'titulo' in row and 'resumen' in row:
                st.write(f"**Título:** {row['titulo']}")
                st.write(f"**Enlace:** [Ver video]({row['enlace']})")
                # Usar st.expander para hacer el resumen colapsable
                with st.expander("Ver resumen"):
                    st.write(row['resumen'])
                st.markdown('---')
            else:
                st.warning(f"Se encontró un resultado sin la información completa en el índice: {index}")
                st.markdown('---')
    else:
        st.info('No se encontraron videos con ese contenido.')
