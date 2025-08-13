# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 08:55:54 2025

@author: dsanm
"""

import streamlit as st
import pandas as pd

# URL del archivo raw en GitHub
url_github = 'https://raw.githubusercontent.com/tu-usuario/tu-repo/main/videos.json'

# Cargar los datos desde GitHub
try:
    df = pd.read_csv(url_github)
    st.success('Datos cargados correctamente desde GitHub.')
except Exception as e:
    st.error(f'Error al cargar los datos: {e}')
    st.stop()

# Título de la aplicación
st.title('🔎 Buscador de videos de YouTube')
st.markdown('---')

# Campo de búsqueda
busqueda = st.text_input('Escribe lo que quieres buscar en los videos:', '')

# Lógica de búsqueda
if busqueda:
    # Buscar en las columnas 'resumen' y 'transcripcion'
    resultados = df[
        df['resumen'].str.contains(busqueda, case=False, na=False) |
        df['transcripcion'].str.contains(busqueda, case=False, na=False)
    ]

    if not resultados.empty:
        st.subheader(f'Videos que coinciden con "{busqueda}":')
        # Mostrar los resultados
        for index, row in resultados.iterrows():
            st.write(f"**Título:** {row['titulo']}")
            st.write(f"**Enlace:** [Ver video]({row['enlace']})")
            st.markdown('---')
    else:
        st.info('No se encontraron videos con ese contenido.')