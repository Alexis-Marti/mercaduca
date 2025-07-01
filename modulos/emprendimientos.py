import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def obtener_emprendimientos():
    """Obtiene todos los registros de EMPRENDIMIENTO de la base de datos."""
    try:
        con = obtener_conexion()
        df = pd.read_sql("SELECT * FROM EMPRENDIMIENTO", con)
        con.close()
        return df
    except Exception as e:
        st.error(f"❌ Error al obtener datos: {e}")
        return pd.DataFrame()

def actualizar_emprendimiento(df):
    """Actualiza los registros de EMPRENDIMIENTO en la base de datos."""
    try:
        con = obtener_conexion()
        cursor = con.cursor()
        registros_actualizados = 0

        for _, row in df.iterrows():
            cursor.execute("""
                UPDATE EMPRENDIMIENTO 
                SET Nombre_emprendimiento=%s,
                    Nombre_emprendedor=%s,
                    Telefono=%s,
                    Estado=%s
                WHERE ID_Emprendimiento=%s
            """, (
                row["Nombre_emprendimiento"],
                row["Nombre_emprendedor"],
                row["Telefono"],
                row["Estado"],
                row["ID_Emprendimiento"]
            ))
            registros_actualizados += cursor.rowcount

        con.commit()
        cursor.close()
        con.close()

        if registros_actualizados > 0:
            st.success(f"✅ Cambios guardados correctamente ({registros_actualizados} registro(s) actualizado(s)).")
        else:
            st.warning("⚠️ No hubo registros actualizados. Verifica que los ID coincidan.")

    except Exception as e:
        st.error(f"❌ Error al actualizar: {e}")

def eliminar_emprendimientos(ids_a_eliminar):
    """Elimina emprendimientos por sus ID desde la base de datos."""
    try:
        con = obtener_conexion()
        cursor = con.cursor()

        formato_ids = ','.join(['%s'] * len(ids_a_eliminar))
        sql = f"DELETE FROM EMPRENDIMIENTO WHERE ID_Emprendimiento IN ({formato_ids})"
        cursor.execute(sql, tuple(ids_a_eliminar))
        registros_eliminados = cursor.rowcount

        con.commit()
        cursor.close()
        con.close()

        if registros_eliminados > 0:
            st.success(f"🗑️ Se eliminaron {registros_eliminados} emprendimiento(s).")
        else:
            st.warning("⚠️ No se eliminó ningún registro. Verifica los ID seleccionados.")
    except Exception as e:
        st.error(f"❌ Error al eliminar: {e}")

def mostrar_emprendimientos():
    """Muestra la tabla de EMPRENDIMIENTOS para permitir edición y eliminación."""
    st.header("📋 Emprendimientos registrados")

    df = obtener_emprendimientos()
    if df.empty:
        st.info("No hay emprendimientos registrados.")
        return

    # Filtro por nombre del emprendimiento con barra buscadora
    nombres_unicos = df["Nombre_emprendimiento"].dropna().unique()
    nombre_seleccionado = st.selectbox(
        "🔍 Buscar emprendimiento por nombre:",
        options=["Todos"] + sorted(nombres_unicos.tolist()),
        index=0
    )

    if nombre_seleccionado != "Todos":
        df = df[df["Nombre_emprendimiento"] == nombre_seleccionado]

    # Agregar columna de eliminación
    df["Eliminar"] = False
    edited_df = st.data_editor(df, num_rows="fixed", use_container_width=True, key="editor_emprendimientos")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Guardar Cambios"):
            actualizar_emprendimiento(edited_df.drop(columns=["Eliminar"]))

    with col2:
        if st.button("🗑️ Eliminar seleccionados"):
            ids_a_eliminar = edited_df[edited_df["Eliminar"] == True]["ID_Emprendimiento"].tolist()
            if ids_a_eliminar:
                eliminar_emprendimientos(ids_a_eliminar)
            else:
                st.info("Selecciona al menos un emprendimiento para eliminar.")


