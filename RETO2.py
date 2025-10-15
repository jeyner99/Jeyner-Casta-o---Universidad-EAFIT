# -*- coding: utf-8 -*-
"""
Reto 2 introducción a la BI - Jeyner Castaño

Este archivo corresponde a una actividad propuesta en introducción a la inteligencia de negocios, la actividad consiste
en la creación de una página con la librería streamlit, página la cual servirá para realizar consultas en lenguaje SQL
gracias a una librería creada en clase llamada SQLib, consultas en una base de datos de contabilidad creada para la materia 
"""

import streamlit as st 
import pandas as pd
import numpy as np
import SQLib as sq
import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime




#Títulos y descripción ---------------------------

st.set_page_config(page_title = "QuimQuinAgro información financiera", layout = "wide")

st.title("QuimQuinAgro información financiera") #Muestra el título en la pestaña

st.write("En esta página podrás consultar informaciónn financiera de QuimQuinAgro de manera eficiente mediante una base de datos actualizada en tiempo real")



# Creamos las pestañas
tab1, tab2, tab3 = st.tabs(["Salidas y entradas de efectivo(caja)", "Egresos", "Socios"])


#voy a crear una pestaña para cada una de las consultas con la intenación de que sea más organizado

with tab1: #Q1

    rango_fechas = st.date_input("Seleccione el rango de fechas entre los cuales quiere consultar entradas y salidas de efectivo:", value=(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)))#Esta línea define una variable llamada rango fechas
    #la variable utiliza un input de streamlit que deja ingresar fechas con un formato predeterminado y las almacena en una lista
    
    
    if len(rango_fechas) == 2: #este if quiere decir que si el tamaño de la lista es de 2 (es decir que tiene 2 entradas, las cuales serían fecha inicial y la final)
        fechainicial = rango_fechas[0].strftime("%Y-%m-%d") #selecciona el primer elemento de la lista el cual sería la fecha inicial y las transforma en texto con formato sql
        fechafinal = rango_fechas[1].strftime("%Y-%m-%d") #selecciona el segundo elemento de la lista el cual sería la fecha final y las transforma en texto con formato sql
    
        consulta_eys = f"SELECT fecha, categoria, entrada, salida FROM edr2025 WHERE fecha BETWEEN '{fechainicial}' AND '{fechafinal}' ORDER BY fecha ASC" #define la consulta la cual haremos con nuestra librería
        
        consultaF = sq.ejecutar_consulta(consulta_eys, "contabilidad.db")
        
        columnas = ["Fecha", "categoría", "entrada", "salida"] #esto es para transformar la consulta en una tabla de datos
        df = pd.DataFrame(consultaF, columns=columnas) #con la finalidad de que se vea más ordenado, pd.Dataframe recibe como filas la consulta y como columnas las columnas que definimos
        
        st.dataframe(df)
        
        #Realizamos el grafico de barras
        
        df["Fecha"] = pd.to_datetime(df["Fecha"]) #convertimos la columna Fecha en formato de fecha
        
        df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)

        df_mes = df.groupby("Mes")[["entrada", "salida"]].sum().reset_index() #Suma las entradas y las salidas de cada mes
        
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_mes["Mes"], y=df_mes["entrada"], name="Entradas", marker_color="green"))
        fig.add_trace(go.Bar(x=df_mes["Mes"], y=df_mes["salida"], name="Salidas", marker_color="red"))
        
        fig.update_layout(
            title="Entradas y salidas de efectivo por mes",
            xaxis_title="Mes",
            yaxis_title="Valor total",
            barmode="group",  # barras lado a lado
            template="plotly_white"
        )
        
        st.plotly_chart(fig)
        
        st.write("Conclusión: podemos observar como se comportan las entradas y las salidas de dinero de la empresa")
        st.write("Esta información será valiosa a la hora de tomar decisiones que afectan el rumbo de la organización, en este caso vemos como durante el año las salidas de efectivo fueron mayores que las entradas, lo cual podría representar problemas de solvencia en un futuro próximo")
        
        
        

with tab2: #Q2
    
    st.write("Aquí podrá consultar y visualizar los 10 mayores egresos ordenados de mayor a menor de la fecha la cual ingrese")
    
    rango_fechas = st.date_input("Seleccione el rango de fechas entre los cuales quiere consultar egresos:",  value=(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)))#Esta línea define una variable llamada rango fechas
    #la variable utiliza un input de streamlit que deja ingresar fechas con un formato predeterminado y las almacena en una lista
    #Definí un valor predeterminado para que quienes entren a la página visualicen los datos y los filtren después
    
    if len(rango_fechas) == 2: 
        fechainicial = rango_fechas[0].strftime("%Y-%m-%d")
        fechafinal = rango_fechas[1].strftime("%Y-%m-%d")
        
        consulta_eys = f"SELECT fecha, categoria, detalle, salida FROM edr2025 WHERE fecha BETWEEN '{fechainicial}' AND '{fechafinal}' ORDER BY salida DESC LIMIT 10"
        
        consultaF = sq.ejecutar_consulta(consulta_eys, "contabilidad.db")
        
        columnas = ["Fecha", "categoría","detalle", "egreso"] #esto es para transformar la consulta en una tabla de datos
        
        df = pd.DataFrame(consultaF, columns=columnas) #con la finalidad de que se vea más ordenado, pd.Dataframe recibe como filas la consulta y como columnas las columnas que definimos
        
        st.dataframe(df)
        
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        
        fig = go.Figure() #aquí creo el gráfico
        
        fig.add_trace(go.Bar( #esta función lo que hace es añadir las características del gráfico a la variable que creamos para el gráfico
            x=df["Fecha"],
            y=df["egreso"],
            marker_color="#1f77b4",  # color azul por defecto
            hovertemplate="<b>Fecha:</b> %{x}<br><b>Egreso:</b> %{y}<extra></extra>"
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("Conclsuión: Esta pestaña nos permite observar los egresos más altos segun la fecha que seleccionemos")
        st.write("Esta información es muy valiosa a la hora de controlar los costos de la organización, permite a quienes toman las decisiones sobre costos identificar en que actividades se están utilizando más recursos y tomar una decisión al respecto")
        

        
with tab3: #Q3

    st.write("Aquí podrá consultar y visualizar los 5 socios de la empresa con mayor aporte a capital social(Socios con aportes mayores a 100 mil pesos)")
    
    socios = st.checkbox("Mostrar los Socios", value = True)
    
    if socios == True:
        
        consulta_soc = f"SELECT nombre, fecha, saldo FROM socios2020 WHERE saldo >= 100000 ORDER BY saldo DESC LIMIT 5 "
        
        consultaS = sq.ejecutar_consulta(consulta_soc, "contabilidad.db")
        
        columnas = ["Nombre socios", "Fecha", "Capital aportado"]
        
        df = pd.DataFrame(consultaS, columns = columnas)
        
        df["Nombre socios"] = df["Nombre socios"].replace({"nn": "Ánonimo","socios/amanda murillas": "Amanda Murillas",  "socios/luis ernesto granada": "Luis Ernesto Granada", "maria julieth madrid": "Maria Julieth Madrid", "amparo cano gomez": "Amparo Cano Gomez"})
    
        seleccionados = []
        for socio in df["Nombre socios"]:
            if st.checkbox(socio, value=True, key=socio):
                seleccionados.append(socio)
                    
                    
        df = df[df["Nombre socios"].isin(seleccionados)]
        
        

        st.dataframe(df)
        
        if not df.empty: #Esta linea sirve para que el gráfico se realice si la tabla tiene datos, esto es porque puede que no haya
        #ningún socio seleccionado y se produzca un error, por eso es que si no hay socios no se grafica
            fig = go.Figure()
        
            fig.add_trace(go.Bar(
                x=df["Nombre socios"],
                y=df["Capital aportado"],
                marker_color="#1f77b4",
                text=df["Capital aportado"],
                textposition="outside",
                hovertemplate="<b>Socio:</b> %{x}<br><b>Capital:</b> %{y}<extra></extra>"
            ))
        
            fig.update_layout(
                title="Capital aportado por socio",
                xaxis_title="Socio",
                yaxis_title="Capital aportado",
                template="plotly_dark",
                height=450
            )
        
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay socios seleccionados para mostrar en el gráfico.")
        
        st.write("Conclusión: esta pestaña nos permite visualizar a los socios que más han invertido en la organización")
        st.write("Esta información será útil al momento de repartir las ganancias, o de identificar los aportes de los socios en momentos los que no está claro de quién es un dinero de la organización o a determinar quienes tienen más poder de decisión")
        
                
        
        
       
        
    
        
    
        
        
    

    