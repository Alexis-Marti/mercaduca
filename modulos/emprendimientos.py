import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def obtener_emprendimientos():
    """Obtiene todos los registros de EMPRENDIMIENTO de la base de datos."""
    con = obtener_conexion()
    df = pd.read_sql("SELECT * FROM EMPRENDIMIENTO", con)
    con.close()
    return df

def actualizar_emprendimiento(df):
    """Actualiza los registros de EMPRENDIMIENTO en la base de datos."""
    con = obtener_conexion()
    cursor = con.cursor()
    registros_actualizados = 0

    df = df.fillna('')  # Evita NaN

    for _, row in df.iterrows():
        try:
            valores = (
                row["Nombre_emprendimiento"],
                row["Nombre_emprendedor"],
                row["Telefono"],
                row["Cuenta_bancaria"],
                row["Estado"],
                row["ID_Emprendimiento"]
            )

            st.write(f"Actualizando con valores: {valores}")  # Mostrar en la app para debug
            cursor.execute("""
                UPDATE EMPRENDIMIENTO 
                SET Nombre_emprendimiento=?,
                    Nombre_emprendedor=?,
                    Telefono=?,
                    Cuenta_bancaria=?,
                    Estado=?
                WHERE ID_Emprendimiento=?
            """, valores)

            registros_actualizados += cursor.rowcount

        except Exception as e:
            st.error(f"❌ Error al actualizar ID {row['ID_Emprendimiento']}: {e}")

    con.commit()
    con.close()

    if registros_actualizados > 0:
        st.success(f"✅ Cambios guardados correctamente ({registros_actualizados} registro(s) actualizado(s)).")
    else:
        st.warning("⚠️ No hubo registros actualizados. Verifica que los ID coincidan.")

def eliminar_emprendimientos(ids_a_eliminar):
    """Elimina emprendimientos por sus ID desde la base de datos."""
    con = obtener_conexion()
    cursor = con.cursor()

    try:
        formato_ids = ','.join(['?'] * len(ids_a_eliminar))
        st.write(f"Eliminando IDs: {ids_a_eliminar}")  # Mostrar en app para debug

        cursor.execute(
            f"DELETE FROM EMPRENDIMIENTO WHERE ID_Emprendimiento IN ({formato_ids})",
            tuple(ids_a_eliminar)
        )

        registros_eliminados = cursor.rowcount

    except Exception as e:
        st.error(f"❌ Error al eliminar: {e}")
        registros_eliminados = 0

    con.commit()
    con.close()

    if registros_eliminados > 0:
        st.success(f"🗑️ Se eliminaron {registros_eliminados} emprendimiento(s).")
    else:
        st.warning("⚠️ No se eliminó ningún registro. Verifica los ID seleccionados.")

def mostrar_emprendimientos():
    """Muestra la tabla de EMPRENDIMIENTOS para permitir edición y eliminación."""
    st.header("📋 Emprendimientos registrados")

    df = obtener_emprendimientos()
    if df.empty:
        st.info("No hay emprendimientos registrados.")
        return

    # Filtro por nombre del emprendimiento con barra buscadora
    nombres_unicos = df["Nombre_emprendimiento"].unique()
    nombre_seleccionado = st.selectbox(
        "🔍 Buscar emprendimiento por nombre:",
        options=["Todos"] + sorted(nombres_unicos.tolist()),
        index=0
    )

    if nombre_seleccionado != "Todos":
        df = df[df["Nombre_emprendimiento"] == nombre_seleccionado]

    # Agregar columna para eliminación
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
