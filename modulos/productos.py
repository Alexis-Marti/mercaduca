import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def obtener_productos():
    """Obtiene todos los registros de PRODUCTO desde la base de datos."""
    con = obtener_conexion()
    df = pd.read_sql("SELECT * FROM PRODUCTO", con)
    con.close()
    return df

def actualizar_productos(df):
    """Actualiza los registros de PRODUCTO en la base de datos."""
    con = obtener_conexion()
    cursor = con.cursor()
    registros_actualizados = 0

    for _, row in df.iterrows():
        cursor.execute("""
            UPDATE PRODUCTO 
            SET Nombre_producto=%s,
                Descripcion=%s,
                Precio=%s,
                Tipo_producto=%s,
                ID_Emprendimiento=%s
            WHERE ID_Producto=%s
        """, (
            str(row["Nombre_producto"]),
            str(row["Descripcion"]),
            float(row["Precio"]),
            str(row["Tipo_producto"]),
            str(row["ID_Emprendimiento"]),
            str(row["ID_Producto"])
        ))

        registros_actualizados += cursor.rowcount

    con.commit()
    con.close()

    if registros_actualizados > 0:
        st.success(f"✅ Cambios guardados correctamente ({registros_actualizados} registro(s) actualizado(s)).")
    else:
        st.warning("⚠️ No hubo registros actualizados. Verifica que los ID coincidan.")

def eliminar_productos(ids_a_eliminar):
    """Elimina productos por sus ID desde la base de datos."""
    con = obtener_conexion()
    cursor = con.cursor()
    formato_ids = ','.join(['%s'] * len(ids_a_eliminar))

    cursor.e

