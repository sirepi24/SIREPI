# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import altair as alt
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1j1xOUF1c2nugU4YyoArWpSwa4u8zfV03YLiVh6sG1PE/edit?usp=sharing"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, worksheet="0")
st.dataframe(data)
st.subheader("PRIMER INDICADOR: Porcentaje de gestantes atendidas")
#if st.button("Suma total"):
sql = 'SELECT ANY_VALUE(PROVINCIA) as PROVINCIA, SUM("DenGest1eraATC") AS GESTANTES, SUM("NumGest1eraATC_1erTri") AS GESTANTES1TRI,(SUM("NumGest1eraATC_1erTri")*100)/SUM("DenGest1eraATC") AS PORCENTAJE  FROM HIS GROUP BY PROVINCIA;'
total_orden = conn.query(sql=sql, spreadsheet=url)
st.dataframe(total_orden)

st.subheader("SEGUNDO INDICADOR: Porcentaje de niños y niñas de 4 meses")
sql1 = 'SELECT ANY_VALUE(PROVINCIA) as PROVINCIA, SUM("Den4mes") AS Den4mes, SUM("Num4mes") AS Num4mes, (SUM("Num4mes")*100)/SUM("Den4mes") AS PORCENTAJE FROM HIS GROUP BY PROVINCIA;'
total_orden1 = conn.query(sql=sql1, spreadsheet=url)
st.dataframe(total_orden1)

st.subheader("TERCER INDICADOR: Porcentaje de de niños y niñas de 12 meses con CRED")
sql2 = 'SELECT ANY_VALUE(PROVINCIA) as PROVINCIA, SUM("DenCREDmes") AS DenCREDmes, SUM("NumCREDmes") AS NumCREDmes, (SUM("NumCREDmes")*100)/SUM("DenCREDmes") AS PORCENTAJE FROM HIS GROUP BY PROVINCIA;'
total_orden2 = conn.query(sql=sql2, spreadsheet=url)
st.dataframe(total_orden2)




