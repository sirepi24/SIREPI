# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1HA8DtdlzlTj0sEsNVtQaZXmpSrhUn3gr3B_g7LMCGTY/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, worksheet="0")

url1 = "https://docs.google.com/spreadsheets/d/1j1xOUF1c2nugU4YyoArWpSwa4u8zfV03YLiVh6sG1PE/edit?usp=sharing"
conn1 = st.connection("gsheets", type=GSheetsConnection)
data1 = conn1.read(spreadsheet=url1, worksheet="0")

st.title("INDICADORES")
genre = st.radio(
    "Eliga una de las anternativas:",
    ["***AGUA***", "***SALUD***", "***EDUCACION***", "***ARTICULACION***"],
    index=None,
    key="horizontal"
)

if genre == '***AGUA***':
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

elif genre == '***SALUD***':
    st.subheader("PRIMER INDICADOR: Porcentaje de gestantes atendidas")
    sql1 = 'SELECT ANY_VALUE(SUB_REGION) as SUB_REGION, ANY_VALUE(PROVINCIA) as PROVINCIA, ANY_VALUE(DISTRITO) as DISTRITO, SUM("DenGest1eraATC") AS GESTANTES, SUM("NumGest1eraATC_1erTri") AS GESTANTES1TRI,(SUM("NumGest1eraATC_1erTri")*100)/SUM("DenGest1eraATC") AS PORCENTAJE  FROM HIS GROUP BY DISTRITO;'
    total_orden = conn1.query(sql=sql1, spreadsheet=url1)
    st.dataframe(total_orden)

    st.subheader("SEGUNDO INDICADOR: Porcentaje de niños y niñas de 4 meses")
    sql2 = 'SELECT ANY_VALUE(SUB_REGION) as SUB_REGION, ANY_VALUE(PROVINCIA) as PROVINCIA, ANY_VALUE(DISTRITO) as DISTRITO,SUM("Den4mes") AS Den4mes, SUM("Num4mes") AS Num4mes, (SUM("Num4mes")*100)/SUM("Den4mes") AS PORCENTAJE FROM HIS GROUP BY DISTRITO;'
    total_orden1 = conn1.query(sql=sql2, spreadsheet=url1)
    st.dataframe(total_orden1)

    st.subheader("TERCER INDICADOR: Porcentaje de de niños y niñas de 12 meses con CRED")
    sql3 = 'SELECT ANY_VALUE(SUB_REGION) as SUB_REGION, ANY_VALUE(PROVINCIA) as PROVINCIA, ANY_VALUE(DISTRITO) as DISTRITO, SUM("DenCREDmes") AS DenCREDmes, SUM("NumCREDmes") AS NumCREDmes, (SUM("NumCREDmes")*100)/SUM("DenCREDmes") AS PORCENTAJE FROM HIS GROUP BY DISTRITO;'
    total_orden2 = conn1.query(sql=sql3, spreadsheet=url1)
    st.dataframe(total_orden2)

