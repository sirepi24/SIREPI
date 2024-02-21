# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1HA8DtdlzlTj0sEsNVtQaZXmpSrhUn3gr3B_g7LMCGTY/edit?usp=sharing"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, worksheet="0")
#st.dataframe(data)
st.subheader("ACCESO AL AGUA CLORADA PARA CONSUMO HUMANO(cloro residual en muestra de agua de consumo >=0.5 MG/L) 2024")
sql = '''
SELECT
    *
FROM 
    Data
WHERE 
    "Cloro" >= '0.5' and "Turbiedad" <= '5'

'''
df_sql_server = conn.query(spreadsheet=url, sql=sql)
#st.dataframe(df_sql_server)

Distrito = st.sidebar.multiselect(
    "Seleccion el Distrito",
    options = data["Distrito"].unique(),
)
st.subheader("Resultados por Distrito")

df_selection_c = data.query(
    "Distrito == @Distrito"
)
st.dataframe(df_selection_c)
st.subheader("SEGUNDO INDICADOR:")
st.subheader("***Numero de centros poblados que realizaron cloración por Provincia***")
sql = 'SELECT ANY_VALUE(Provincia) as PROVINCIA, COUNT("Nombre CCPP") AS NumCentrosPoblados FROM Data GROUP BY Provincia ORDER BY Provincia ASC;'
total_orden = conn.query(sql=sql, spreadsheet=url)
st.dataframe(total_orden)

st.subheader("***Numero de centros poblados que realizaron cloración por Distrito***")
sql = 'SELECT ANY_VALUE(Provincia) as PROVINCIA, ANY_VALUE(Distrito) as DISTRITO, COUNT("Nombre CCPP") AS NumCentrosPoblados FROM Data GROUP BY Distrito ORDER BY Provincia ASC;'
total_orden = conn.query(sql=sql, spreadsheet=url)
st.dataframe(total_orden)