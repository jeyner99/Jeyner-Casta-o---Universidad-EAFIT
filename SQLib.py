# -*- coding: utf-8 -*-
"""
Editor de Spyder



Este es un archivo temporal.
"""

import pandas as pd
import sqlite3
import os

def archivo_a_sql(ruta_archivo, nombre_db):
    """
    

    Parameters
    ----------
    ruta_archivo : TYPE
        DESCRIPTION.
    nombre_db : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    try:
        
        # Conectamos a la base de datos
        # Creamos un conectar llamado  conn a la base de datos
        conn = sqlite3.connect(nombre_db)
        
        cursor = conn.cursor()
        
        # Revisamos la extensión del archivo del usuario
        extension = os.path.splitext(ruta_archivo)[1].lower()  
        
        if extension in ['.xlsx', '.xls']:
            
            #Procesamos el archivo excel
            # Almacenamos en la variable xls los datos del arfchivo
            xls = pd.ExcelFile(ruta_archivo)
            #Hacemos un ciclo que recorra cada hoja de calculo
            
            for sheet_name in xls.sheet_names:
                # Almacenamos el contenido de cada hoja de cálculo en la vaariable df
                df = pd.read.excel(ruta_archivo, sheet_name)
    
            # Guardamos el nombre de la hoja de cálculo para convertirlo en el nombre de la tabla
            
            table_name = sheet_name.strip().replace(' ','_').replace('-','_')
            # Llevamos el contenido de df a la tabla de sql
            df.to.sql(table_name, conn, if_exists = 'replace', index = False)
            
            print(f"Hoja  '{sheet_name}' importada con éxito")
            
        elif extension == '.csv':
            # Procesamos el archivo CSV
            # Llevamos el contenido del archivo a la variable
            df = pd.read_csv(ruta_archivo)
            #Generamos el nombre de la tabla
            table_name = os.path.splitext(os.path.basename(ruta_archivo))[0].replace(' ','_').replace('-','_')
            
            df.to_sql(table_name, conn, if_exists = 'replace', index = False)
            
            print(f"La tabla '{table_name}' fue importada con éxito")
            
        else: 
            print("El formato de archivo no es compatible")
            
    except:
        print("Error durante la conversión")
        
    finally:
        # Cerramos la conexión de la base de datos
        conn.close()
        print("Conexión cerrada")
        

def ejecutar_consulta(consulta_sql, nombre_db):
    """
    Ejecuta una consulta SQL sobre una base de datpos SQLite3
    
    Parameters
    ----------
    consulta_sql : string(str) consulta a ejecutar
    nombre_db : string(str) nombre de la base de datos SQLite3

    Returns
    -------
    resultado_consulta: string, dataframe resultado de la consulta

    """
    
    try:
        #conectamos con la base de datos
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()
        
        # Ejecutamos la consulta ingresada por el usuario
        cursor.execute(consulta_sql)
        
        # Verificamos si es una consulta tipo SELECT
        
        if consulta_sql.strip().lower().startswith('select'):
            resultado_consulta = cursor.fetchall()
            return resultado_consulta
        
        else:
            # Confirmamos los cambios para INSERT, UPDATE, DELETE
            conn.commit()
            return None
        
    except:
        print("Error en la ejecución")
        return None
    
    finally:
        #Cerramos la conexión
        conn.close()
        print("Conexión cerrada")
        
def mostrar_tablas(nombre_db):
    """
    Muestra todas las tablas de la  base de datos nombre_db

    Parameters
    ----------
    nombre_db : string (str) nombre de la base de datos
    
    

    Returns
    -------
        : list lista con los nnombres de las tablas de la base de datos
        

    """
    try: 
        # Establecemos la conexión con la base de datos
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()
        
        # Ejecutamos una consulta 
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'; ")
       
        tablas = cursor.fetchall()
        #retornamos la lista de las tablas
        return [tabla[0] for tabla in tablas]
    
    except: 
        print("Error en la consulta de las tablas")        
        
    finally:
        conn.close()
        print("Cerramos la conexión")