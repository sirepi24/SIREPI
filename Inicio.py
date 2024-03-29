# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1HA8DtdlzlTj0sEsNVtQaZXmpSrhUn3gr3B_g7LMCGTY/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url, worksheet="0")

url1 = "https://docs.google.com/spreadsheets/d/1j1xOUF1c2nugU4YyoArWpSwa4u8zfV03YLiVh6sG1PE/edit?usp=sharing"
conn1 = st.connection("gsheets", type=GSheetsConnection)
data1 = conn1.read(spreadsheet=url1, worksheet="0")

st.title("SISTEMA REGIONAL DE ATENCION INFANTIL DE LA PRIMERA INFANCIA")
st.title("INDICADORES")
genre = st.radio(
    "Eliga una de las anternativas:",
    ["***AGUA***", "***SALUD***", "***EDUCACION***", "***ARTICULACION***"],
    index=None,
    key="horizontal"
)

if genre == '***AGUA***':
    st.subheader("ACCESO AL AGUA CLORADA PARA CONSUMO HUMANO(cloro residual en muestra de agua de consumo >=0.5 MG/L) 2024")
    sql = '''SELECT ANY_VALUE("Provincia") as Provincia, ANY_VALUE("Distrito") as Distrito,COUNT(DISTINCT "Nombre CCPP") as Numero_de_CCPP_que_realizaron_cloracion FROM Data WHERE "Cloro" >= '0,5' GROUP BY "Distrito" ORDER BY "Provincia" '''
    df_sql_server = conn.query(sql=sql, spreadsheet=url)
    st.dataframe(df_sql_server)


elif genre == '***SALUD***':
    st.subheader("PRIMER INDICADOR: Porcentaje de gestantes atendidas")
    #if st.button("Suma total"):
    sql = 'SELECT ANY_VALUE(SUB_REGION) as SUB_REGION, ANY_VALUE(PROVINCIA) as PROVINCIA, ANY_VALUE(DISTRITO) as DISTRITO, SUM("DenGest1eraATC") AS GESTANTES, SUM("NumGest1eraATC_1erTri") AS GESTANTES1TRI,(SUM("NumGest1eraATC_1erTri")*100)/SUM("DenGest1eraATC") AS PORCENTAJE  FROM HIS GROUP BY DISTRITO;'
    total_orden = conn.query(sql=sql, spreadsheet=url1)
    st.dataframe(total_orden)

    DISTRITO = st.sidebar.multiselect(
        "Seleccion el Distrito",
        options = total_orden["DISTRITO"].unique(),
    )
    st.subheader("Resultados por Distrito")

    df_selection_c = total_orden.query(
        "DISTRITO == @DISTRITO"
    )
    st.dataframe(df_selection_c)

    st.subheader("SEGUNDO INDICADOR: Porcentaje de niños y niñas de 4 meses")
    sql1 = 'SELECT ANY_VALUE(SUB_REGION) as SUB_REGION, ANY_VALUE(PROVINCIA) as PROVINCIA, ANY_VALUE(DISTRITO) as DISTRITO,SUM("Den4mes") AS Den4mes, SUM("Num4mes") AS Num4mes, (SUM("Num4mes")*100)/SUM("Den4mes") AS PORCENTAJE FROM HIS GROUP BY DISTRITO;'
    total_orden1 = conn.query(sql=sql1, spreadsheet=url1)
    st.dataframe(total_orden1)

    DISTRITO1 = st.sidebar.multiselect(
        "Seleccion el Distrito",
        options = total_orden1["DISTRITO"].unique(),
    )

    st.subheader("Resultados por Distrito")

    df_selection_c1 = total_orden1.query(
        "DISTRITO == @DISTRITO1"
    )
    st.dataframe(df_selection_c1)

    st.subheader("TERCER INDICADOR: Porcentaje de de niños y niñas de 12 meses con CRED")
    sql2 = 'SELECT ANY_VALUE(SUB_REGION) as SUB_REGION, ANY_VALUE(PROVINCIA) as PROVINCIA, ANY_VALUE(DISTRITO) as DISTRITO, SUM("DenCREDmes") AS DenCREDmes, SUM("NumCREDmes") AS NumCREDmes, (SUM("NumCREDmes")*100)/SUM("DenCREDmes") AS PORCENTAJE FROM HIS GROUP BY DISTRITO;'
    total_orden2 = conn.query(sql=sql2, spreadsheet=url1)
    st.dataframe(total_orden2)

    DISTRITO2 = st.sidebar.multiselect(
        "Seleccion el Distrito",
        options = total_orden2["DISTRITO"].unique(),
    )

    st.subheader("Resultados por Distrito")

    df_selection_c2 = total_orden2.query(
        "DISTRITO == @DISTRITO2"
    )
    st.dataframe(df_selection_c2)

